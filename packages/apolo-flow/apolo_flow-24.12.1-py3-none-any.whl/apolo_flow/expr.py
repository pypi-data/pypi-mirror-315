# expression parser/evaluator
# ${{ <expression> }}
import dataclasses

import abc
import asyncio
import collections
import collections.abc
import datetime
import enum
import hashlib
import inspect
import json
import operator
import re
import shlex
from abc import ABC
from apolo_sdk import Client, JobDescription, JobRestartPolicy, JobStatus
from ast import literal_eval
from collections.abc import Sized
from contextlib import asynccontextmanager
from funcparserlib.parser import (
    Parser,
    finished,
    forward_decl,
    many,
    maybe,
    oneplus,
    skip,
    some,
)
from typing import (
    Any,
    AsyncContextManager,
    AsyncIterator,
    Awaitable,
    Callable,
    ClassVar,
    Dict,
    Generic,
    Iterable,
    Iterator,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
    cast,
)
from typing_extensions import Final, Protocol, runtime_checkable
from yarl import URL

from .tokenizer import Pos, Token, tokenize
from .types import AlwaysT, LocalPath, RemotePath, TaskStatus
from .utils import run_subproc


LiteralT = Union[None, bool, int, float, str]

TypeT = Union[
    LiteralT,
    "ContainerT",
    "MappingT",
    "SequenceT",
    LocalPath,
    RemotePath,
    URL,
    AlwaysT,
]

_T = TypeVar("_T", bound=TypeT)
_IT = TypeVar("_IT", bound=TypeT)


@runtime_checkable
class ContainerT(Protocol):
    def __getattr__(self, attr: str) -> TypeT: ...


@runtime_checkable
class MappingT(Protocol):
    def __getitem__(self, key: LiteralT) -> TypeT: ...

    def __iter__(self) -> Iterator[LiteralT]: ...


@runtime_checkable
class SequenceT(Protocol):
    def __getitem__(self, idx: LiteralT) -> TypeT: ...

    def __iter__(self) -> Iterator[TypeT]: ...


class RootABC(abc.ABC):
    @abc.abstractmethod
    def lookup(self, name: str) -> TypeT:
        pass

    @abc.abstractmethod
    def client(self) -> AsyncContextManager[Client]:
        pass

    @property
    @abc.abstractmethod
    def dry_run(self) -> bool: ...


class LocalScope(RootABC):
    def __init__(self, base: RootABC, scope: Mapping[str, TypeT]) -> None:
        self._base = base
        self._scope = scope

    @asynccontextmanager
    async def client(self) -> AsyncIterator[Client]:
        async with self._base.client() as client:
            yield client

    @property
    def dry_run(self) -> bool:
        return self._base.dry_run

    def lookup(self, name: str) -> TypeT:
        if name in self._scope:
            return self._scope[name]
        return self._base.lookup(name)


class EvalError(Exception):
    def __init__(self, msg: str, start: Pos, end: Pos) -> None:
        super().__init__(msg)
        self.start = start
        self.end = end

    @staticmethod
    def format_pos(pos: Pos) -> str:
        # For humans, line and columns are enumerated from 1, so we should add 1 here.
        return f'"{pos.filename}", line {pos.line + 1}, column {pos.col + 1}'

    def __str__(self) -> str:
        return str(self.args[0]) + f"\n  in {self.format_pos(self.start)}"


class MultiError(Exception):
    def __init__(self, errors: Sequence[Exception]):
        self.errors = errors

    def __str__(self) -> str:
        return "\n".join(str(error) for error in self.errors)


def parse_literal(arg: str, err_msg: str) -> LiteralT:
    try:
        return cast(LiteralT, literal_eval(arg))
    except (ValueError, SyntaxError):
        raise ValueError(f"'{arg}' is not " + err_msg)


@dataclasses.dataclass(frozen=True)
class FuncDef:
    name: str
    sig: inspect.Signature
    call: Callable[..., Awaitable[TypeT]]


@dataclasses.dataclass
class CallCtx:
    start: Pos
    end: Pos
    root: RootABC


def _build_signatures(**kwargs: Callable[..., Awaitable[TypeT]]) -> Dict[str, FuncDef]:
    return {k: FuncDef(k, inspect.signature(v), v) for k, v in kwargs.items()}


async def nothing(ctx: CallCtx) -> None:
    # A test function that accepts none args.
    # Later we can replace it with something really more usefuld, e.g. succeded()
    return None


async def alen(ctx: CallCtx, arg: TypeT) -> int:
    # Async version of len(), async is required for the sake of uniformness.
    if not isinstance(arg, Sized):
        raise TypeError(f"len() requires a str, sequence or mapping, got {arg!r}")
    return len(arg)


async def aint(ctx: CallCtx, arg: TypeT) -> int:
    # Async version of int(), async is required for the sake of uniformness.
    if not isinstance(arg, (int, str, float, bool)):
        raise TypeError(f"int() requires a str or a number, got {arg!r}")
    return int(arg)


async def akeys(ctx: CallCtx, arg: TypeT) -> TypeT:
    # Async version of list(), async is required for the sake of uniformness.
    if not isinstance(arg, Mapping):
        raise TypeError(f"keys() requires a mapping, got {arg!r}")
    return list(arg)  # type: ignore  # List[...] is implicitly converted to SequenceT


async def values(ctx: CallCtx, arg: TypeT) -> TypeT:
    # Trampoline for mapping.values, async is required for the sake of uniformness.
    if not isinstance(arg, Mapping):
        raise TypeError(f"values() requires a mapping, got {arg!r}")
    return list(arg.values())  # type: ignore  # implicitly converted to SequenceT


async def arange(
    ctx: CallCtx, arg: TypeT, arg2: Optional[TypeT] = None, arg3: Optional[TypeT] = None
) -> SequenceT:
    if not isinstance(arg, int):
        raise TypeError(f"range() first argument should be an int, got {arg!r}")
    if arg2:
        if not isinstance(arg2, int):
            raise TypeError(f"range() second argument should be an int, got {arg2!r}")
        if arg3:
            if not isinstance(arg3, int):
                raise TypeError(
                    f"range() third argument should be an int, got {arg3!r}"
                )
            return list(range(arg, arg2, arg3))  # type: ignore
        return list(range(arg, arg2))  # type: ignore
    return list(range(arg))  # type: ignore


async def fmt(ctx: CallCtx, spec: str, *args: TypeT) -> str:
    # We need a trampoline since expression syntax doesn't support classes and named
    # argumens
    return spec.format(*args)


class JSONEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if not isinstance(obj, type) and dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj)
        elif isinstance(obj, enum.Enum):
            return obj.value
        elif isinstance(obj, RemotePath):
            return str(obj)
        elif isinstance(obj, LocalPath):
            return str(obj)
        elif isinstance(obj, collections.abc.Set):
            return sorted(obj)
        elif isinstance(obj, AlwaysT):
            return str(obj)
        elif isinstance(obj, URL):
            return str(obj)
        elif isinstance(obj, datetime.datetime):
            return str(obj)
        # Let the base class default method raise the TypeError
        return super().default(obj)


async def to_json(ctx: CallCtx, arg: TypeT) -> str:
    return json.dumps(arg, cls=JSONEncoder)


async def from_json(ctx: CallCtx, arg: str) -> TypeT:
    return cast(TypeT, json.loads(arg))


async def hash_files(ctx: CallCtx, *patterns: str) -> str:
    flow = ctx.root.lookup("flow")
    # emulate attr lookup
    workspace: LocalPath = cast(
        LocalPath,
        await AttrGetter(ctx.start, ctx.end, name="workspace").eval(
            ctx.root, flow, start=ctx.start
        ),
    )
    return await hash_files_relative(ctx, workspace, *patterns)


async def hash_files_relative(ctx: CallCtx, root: LocalPath, *patterns: str) -> str:
    hasher = hashlib.new("sha256")
    buffer = bytearray(16 * 1024 * 1024)  # 16 MB
    view = memoryview(buffer)
    # emulate attr lookup
    for pattern in patterns:
        for fname in sorted(root.glob(pattern)):
            # On Windows the Python 3.6 glob() returns lower-cased filenames,
            # resolve() restores the case.
            relative_fname = fname.resolve().relative_to(root.resolve()).as_posix()
            hasher.update(relative_fname.encode("utf-8"))
            with fname.open("rb", buffering=0) as stream:
                read = stream.readinto(buffer)
                while read:
                    hasher.update(view[:read])
                    read = stream.readinto(buffer)
    return hasher.hexdigest()


async def upload(ctx: CallCtx, volume_ctx: ContainerT) -> ContainerT:
    from .context import VolumeCtx

    if not isinstance(volume_ctx, VolumeCtx):
        raise ValueError("upload() argument should be volume")
    mkdir_cmd = [
        "apolo",
        "mkdir",
        "--parents",
        str(volume_ctx.remote.parent),
    ]
    cp_cmd = [
        "apolo",
        "cp",
        "--recursive",
        "--update",
        "--no-target-directory",
        str(volume_ctx.full_local_path),
        str(volume_ctx.remote),
    ]
    if ctx.root.dry_run:
        print(" ".join(shlex.quote(arg) for arg in mkdir_cmd))
        print(" ".join(shlex.quote(arg) for arg in cp_cmd))
    else:
        await run_subproc(*mkdir_cmd)
        await run_subproc(*cp_cmd)
    return volume_ctx


async def alower(ctx: CallCtx, arg: TypeT) -> str:
    # Async version of lower(), async is required for the sake of uniformness.
    if not isinstance(arg, str):
        raise TypeError(f"lower() requires a str, got {arg!r}")
    return arg.lower()


async def aupper(ctx: CallCtx, arg: TypeT) -> str:
    # Async version of lower(), async is required for the sake of uniformness.
    if not isinstance(arg, str):
        raise TypeError(f"upper() requires a str, got {arg!r}")
    return arg.upper()


async def astr(ctx: CallCtx, arg: TypeT) -> str:
    # Async version of str(), async is required for the sake of uniformness.
    return str(arg)


async def replace(ctx: CallCtx, arg: TypeT, old: TypeT, new: TypeT) -> str:
    # We need a trampoline since expression syntax doesn't support classes
    if not isinstance(arg, str):
        raise TypeError(f"replace() first argument should be a str, got {arg!r}")
    if not isinstance(old, str):
        raise TypeError(f"replace() second argument should be a str, got {old!r}")
    if not isinstance(new, str):
        raise TypeError(f"replace() third argument should be a str, got {new!r}")
    return arg.replace(old, new)


async def join(
    ctx: CallCtx, sep: TypeT, array: TypeT, convert_to_str: TypeT = False
) -> str:
    # We need a trampoline since expression syntax doesn't support classes
    if not isinstance(sep, str):
        raise TypeError(f"join() first argument should be a str, got {sep!r}")
    if not isinstance(array, SequenceT):
        raise TypeError(
            f"replace() second argument should be a sequence, got {array!r}"
        )
    if not isinstance(convert_to_str, bool):
        raise TypeError(
            f"replace() third argument should be a bool, got {convert_to_str!r}"
        )
    str_array = []
    for idx, item in enumerate(array):
        if convert_to_str:
            item = str(item)
        if not isinstance(item, str):
            raise TypeError(f"join() array item {idx} should be a str, got {item!r}")
        str_array.append(item)
    return sep.join(str_array)


async def parse_volume(ctx: CallCtx, arg: TypeT) -> ContainerT:
    from .context import VolumeCtx

    if not isinstance(arg, str):
        raise TypeError(f"parse_volume() requires a str, got {arg!r}")
    async with ctx.root.client() as client:
        volume = client.parse.volume(arg)
    return VolumeCtx(  # type: ignore[return-value]
        id="<volume>",
        remote=volume.storage_uri,
        mount=RemotePath(volume.container_path),
        read_only=volume.read_only,
        local=None,
        full_local_path=None,
    )


def _check_has_needs(ctx: CallCtx, *, func_name: str) -> None:
    try:
        ctx.root.lookup("needs")
    except LookupError:
        raise ValueError(f"{func_name}() is only available inside a task definition")


def _get_needs_statuses(root: RootABC) -> Dict[str, TaskStatus]:
    needs = root.lookup("needs")
    assert isinstance(needs, MappingT)
    result: Dict[str, TaskStatus] = {}
    for dependency in needs:
        dep_ctx = needs[dependency]
        result[dependency] = dep_ctx.result  # type: ignore
    return result


async def always(ctx: CallCtx, *args: str) -> AlwaysT:
    _check_has_needs(ctx, func_name="always")
    return AlwaysT()


async def success(ctx: CallCtx, *args: str) -> bool:
    # When called without arguments, checks that all dependency task
    # succeeded. If arguments are passed, they should be strings that
    # name some task from `needs:` field. Function will return true
    # if all of those tasks succeded.
    _check_has_needs(ctx, func_name="success")
    needs_statuses = _get_needs_statuses(ctx.root)
    if not args:
        return all(status == TaskStatus.SUCCEEDED for status in needs_statuses.values())
    else:
        if not all(isinstance(arg, str) for arg in args):
            raise ValueError("success() function only accept string arguments")
        try:
            return all(needs_statuses[need] == TaskStatus.SUCCEEDED for need in args)
        except KeyError as e:
            raise ValueError(
                "success() function got argument, that"
                f'is not a defined as dependency: "{e.args[0]}"'
            )


async def failure(ctx: CallCtx, *args: str) -> bool:
    # When called without arguments, checks if any of dependency task
    # failed. If arguments are passed, they should be strings that
    # name some task from `needs:` field. Function will return true
    # if any of those tasks failure.
    _check_has_needs(ctx, func_name="failure")
    needs_statuses = _get_needs_statuses(ctx.root)
    if not args:
        return any(status == TaskStatus.FAILED for status in needs_statuses.values())
    else:
        if not all(isinstance(arg, str) for arg in args):
            raise ValueError("failure() function only accept string arguments")
        try:
            return any(needs_statuses[need] == TaskStatus.FAILED for need in args)
        except KeyError as e:
            raise ValueError(
                "failure() function got argument, that"
                f'is not a defined as dependency: "{e.args[0]}"'
            )


async def inspect_job(
    ctx: CallCtx, job_name: TypeT, suffix: Optional[TypeT] = None
) -> ContainerT:
    from .context import LiveContext, _id2tag

    if not isinstance(ctx.root, LiveContext):
        raise ValueError("inspect_job() is only available inside a job definition")
    if not isinstance(job_name, str):
        raise TypeError(
            f"inspect_job() job_name argument should be a str, got {job_name!r}"
        )
    if suffix is not None and not isinstance(suffix, str):
        raise TypeError(
            f"inspect_job() suffix argument should be a str, got {suffix!r}"
        )

    tags = ctx.root.tags | {f"job:{_id2tag(job_name)}"}
    if suffix is not None:
        tags |= {f"multi:{suffix}"}
    found_job: Optional[JobDescription] = None
    async with ctx.root.client() as client:
        async for job in client.jobs.list(
            tags=tags,
            reverse=True,
            limit=1,
            statuses=JobStatus.active_items(),
        ):
            found_job = job
    if found_job is None:
        raise ValueError(
            f"inspect_job() did not found running job with name {job_name}"
            + (f" and suffix {suffix}" if suffix else "")
        )
    return found_job  # type: ignore[return-value]


FUNCTIONS = _build_signatures(
    len=alen,
    int=aint,
    range=arange,
    nothing=nothing,
    fmt=fmt,
    str=astr,
    replace=replace,
    join=join,
    keys=akeys,
    values=values,
    to_json=to_json,
    from_json=from_json,
    success=success,
    failure=failure,
    hash_files=hash_files,
    hash_files_relative=hash_files_relative,
    always=always,
    upload=upload,
    lower=alower,
    upper=aupper,
    parse_volume=parse_volume,
    inspect_job=inspect_job,
)


@dataclasses.dataclass(frozen=True)
class Entity(abc.ABC):
    start: Pos
    end: Pos


class Item(Entity):
    @abc.abstractmethod
    async def eval(self, root: RootABC) -> TypeT:
        pass

    def child_items(self) -> Iterable["Item"]:
        return []


@dataclasses.dataclass(frozen=True)
class Literal(Item):
    val: LiteralT

    async def eval(self, root: RootABC) -> LiteralT:
        return self.val


def make_toktype_predicate(toktype: str) -> Callable[[Token], bool]:
    def _predicate(token: Token) -> bool:
        return token.type == toktype

    return _predicate


def literal(toktype: str) -> "Parser[Token, Literal]":
    def f(tok: Token) -> Literal:
        return Literal(tok.start, tok.end, literal_eval(tok.value))

    return some(make_toktype_predicate(toktype)) >> f


class Getter(Entity):
    # Aux class for Lookup item

    @abc.abstractmethod
    async def eval(self, root: RootABC, obj: TypeT, start: Pos) -> TypeT:
        pass


@dataclasses.dataclass(frozen=True)
class AttrGetter(Getter):
    name: str

    async def eval(self, root: RootABC, obj: TypeT, start: Pos) -> TypeT:
        if dataclasses.is_dataclass(obj):
            name = self.name
            try:
                return cast(TypeT, getattr(obj, name))
            except AttributeError:
                raise EvalError(f"No attribute {self.name}", start, self.end)
        elif isinstance(obj, MappingT):
            try:
                return obj[self.name]
            except KeyError:
                raise EvalError(f"No attribute {self.name}", start, self.end)
        else:
            raise EvalError(
                f"Is not an object with attributes accessible by a dot.",
                start,
                self.end,
            )


def lookup_attr(name: Token) -> Any:
    # Just in case, NAME token cannot start with _.
    assert not name.value.startswith("_")
    return AttrGetter(name.start, name.end, name.value)


@dataclasses.dataclass(frozen=True)
class ItemGetter(Getter):
    key: Item

    async def eval(self, root: RootABC, obj: TypeT, start: Pos) -> TypeT:
        assert isinstance(obj, (SequenceT, MappingT))
        key = cast(LiteralT, await self.key.eval(root))
        try:
            return obj[key]
        except LookupError:
            raise EvalError(f"No item {self.key}", start, self.end)


def lookup_item(key: Item) -> Any:
    return ItemGetter(key.start, key.end, key)


@dataclasses.dataclass(frozen=True)
class Lookup(Item):
    root: str
    trailer: Sequence[Getter]

    async def eval(self, root: RootABC) -> TypeT:
        ret = root.lookup(self.root)
        start = self.start
        for op in self.trailer:
            ret = await op.eval(root, ret, start)
        return ret

    def child_items(self) -> Iterable["Item"]:
        for getter in self.trailer:
            if isinstance(getter, ItemGetter):
                yield getter.key


def make_lookup(arg: Tuple[Token, List[Getter]]) -> Lookup:
    name, trailer = arg
    end = trailer[-1].end if trailer else name.end
    return Lookup(name.start, end, name.value, trailer)


def make_args(arg: Optional[Tuple[Item, List[Item]]]) -> List[Item]:
    if arg is None:
        return []
    first, tail = arg
    return [first] + tail[:]


@dataclasses.dataclass(frozen=True)
class Call(Item):
    func: FuncDef
    args: Sequence[Item]
    trailer: Sequence[Getter]

    async def eval(self, root: RootABC) -> TypeT:
        args = [await a.eval(root) for a in self.args]
        try:
            call_ctx = CallCtx(self.start, self.end, root)
            ret = await self.func.call(call_ctx, *args)
        except asyncio.CancelledError:
            raise
        except EvalError:
            raise
        except Exception as exc:
            raise EvalError(str(exc), self.start, self.end)
        start = self.start
        for op in self.trailer:
            ret = await op.eval(root, ret, start)
        return ret

    def child_items(self) -> Iterable["Item"]:
        yield from self.args
        for getter in self.trailer:
            if isinstance(getter, ItemGetter):
                yield getter.key


def make_call(arg: Tuple[Token, List[Item], Sequence[Getter]]) -> Call:
    funcname, args, trailer = arg
    try:
        spec = FUNCTIONS[funcname.value]
    except KeyError:
        raise LookupError(f"Unknown function {funcname.value}")
    end = funcname.end
    args_count = len(args)
    if args_count > 0:
        end = args[-1].end
    dummies = [None] * args_count
    spec.sig.bind(None, *dummies)
    if trailer:
        end = trailer[-1].end
    return Call(funcname.start, end, spec, args, trailer)


@dataclasses.dataclass(frozen=True)
class Text(Item):
    arg: str

    async def eval(self, root: RootABC) -> str:
        return self.arg


def make_text(arg: Token) -> Text:
    return Text(arg.start, arg.end, arg.value)


@dataclasses.dataclass(frozen=True)
class BinOp(Item):
    op: Callable[[TypeT, TypeT], TypeT]
    left: Item
    right: Item

    async def eval(self, root: RootABC) -> TypeT:
        left_val = await self.left.eval(root)
        right_val = await self.right.eval(root)
        return self.op(left_val, right_val)

    def child_items(self) -> Iterable["Item"]:
        return [self.left, self.right]


def or_(arg1: Any, arg2: Any) -> Any:
    # Emulate dicts concatination from Python 3.9
    d: Mapping[Any, Any]
    if isinstance(arg1, collections.abc.Mapping):
        d = dict(arg1)
        d.update(arg2)
        return d
    elif isinstance(arg2, collections.abc.Mapping):
        d = dict(arg2)
        d.update(arg1)
        return d
    else:
        return operator.or_(arg1, arg2)


def logical_and(arg1: Any, arg2: Any) -> Any:
    return arg1 and arg2


def logical_or(arg1: Any, arg2: Any) -> Any:
    return arg1 or arg2


BinOpTrailer = List[Tuple[Token, Item]]


def make_op_trailer(args: Optional[Tuple[Token, Item, BinOpTrailer]]) -> BinOpTrailer:
    if args is None:
        return []
    op_token, item, trailer = args
    return [(op_token, item), *trailer]


def make_bin_op_expr(args: Tuple[Item, BinOpTrailer]) -> Item:
    op_map = {
        "==": operator.eq,
        "!=": operator.ne,
        "or": logical_or,
        "and": logical_and,
        "<": operator.lt,
        "<=": operator.le,
        ">": operator.gt,
        ">=": operator.ge,
        "|": or_,
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
        "%": operator.mod,
    }

    item, trailer = args
    for op_token, right_item in trailer:
        item = BinOp(
            item.start,
            right_item.end,
            op=op_map[op_token.value],
            left=item,
            right=right_item,
        )
    return item


@dataclasses.dataclass(frozen=True)
class UnaryOp(Item):
    op: Callable[[TypeT], TypeT]
    operand: Item

    async def eval(self, root: RootABC) -> TypeT:
        operand_val = await self.operand.eval(root)
        return self.op(operand_val)

    def child_items(self) -> Iterable["Item"]:
        return [self.operand]


def _unary_plus(arg: Any) -> Any:
    return +arg


def _unary_minus(arg: Any) -> Any:
    return -arg


def make_unary_op_expr(args: Tuple[Token, Item]) -> UnaryOp:
    op_map = {
        "not": operator.not_,
        "+": _unary_plus,
        "-": _unary_minus,
    }
    op_token = args[0]
    return UnaryOp(
        args[0].start,
        args[1].end,
        op=op_map[op_token.value],
        operand=args[1],
    )


@dataclasses.dataclass(frozen=True)
class ListMaker(Item):
    items: Sequence[Item]

    async def eval(self, root: RootABC) -> SequenceT:
        return [await item.eval(root) for item in self.items]  # type: ignore

    def child_items(self) -> Iterable["Item"]:
        return self.items


def make_list(args: Tuple[Item, List[Item]]) -> ListMaker:
    lst = [args[0]] + args[1]
    return ListMaker(lst[0].start, lst[-1].end, lst)


def make_empty_list(args: Tuple[Token, Token]) -> ListMaker:
    return ListMaker(args[0].start, args[1].end, [])


@dataclasses.dataclass(frozen=True)
class ListCompMaker(Item):
    item_expr: Item
    var_name: str
    base_iter: Item
    if_expr: Optional[Item] = None

    async def eval(self, root: RootABC) -> SequenceT:
        res = []
        for value in await self.base_iter.eval(root):  # type: ignore
            subroot = LocalScope(root, {self.var_name: value})
            if self.if_expr and not await self.if_expr.eval(subroot):
                continue
            res.append(await self.item_expr.eval(subroot))
        return res  # type: ignore

    def child_items(self) -> Iterable["Item"]:
        return [self.item_expr, self.base_iter]


def make_list_comp(args: Tuple[Item, Token, Token, Token, Item]) -> ListCompMaker:
    item_expr, _, name, _, base_iter = args
    return ListCompMaker(
        item_expr.start,
        base_iter.end,
        item_expr,
        name.name,
        base_iter,
    )


def make_list_comp_with_if(
    args: Tuple[Item, Token, Token, Token, Item, Token, Item]
) -> ListCompMaker:
    item_expr, _, name, _, base_iter, _, if_expr = args
    return ListCompMaker(
        item_expr.start,
        base_iter.end,
        item_expr,
        name.name,
        base_iter,
        if_expr,
    )


@dataclasses.dataclass(frozen=True)
class DictMaker(Item):
    items: Sequence[Tuple[Item, Item]]

    async def eval(self, root: RootABC) -> MappingT:
        ret = {}
        for key, value in self.items:
            k = await key.eval(root)
            v = await value.eval(root)
            ret[k] = v
        return ret  # type: ignore

    def child_items(self) -> Iterable["Item"]:
        for entry in self.items:
            yield entry[0]
            yield entry[1]


def make_dict(
    args: Union[Tuple[Item, Item, List[Tuple[Item, Item]]], Tuple[Item, Item]]
) -> DictMaker:
    lst = [(args[0], args[1])]
    if len(args) > 2:
        lst += args[2]
    return DictMaker(lst[0][0].start, lst[-1][1].end, lst)


def make_empty_dict(args: Tuple[Token, Token]) -> DictMaker:
    return DictMaker(args[0].start, args[0].end, [])


@dataclasses.dataclass(frozen=True)
class TernaryOp(Item):
    left: Item
    condition: Item
    right: Item

    async def eval(self, root: RootABC) -> TypeT:
        if await self.condition.eval(root):
            return await self.left.eval(root)
        else:
            return await self.right.eval(root)

    def child_items(self) -> Iterable["Item"]:
        return [self.left, self.condition, self.right]


def make_if_else(args: Tuple[Item, Token, Item, Token, Item]) -> TernaryOp:
    return TernaryOp(
        args[0].start,
        args[1].end,
        left=args[0],
        condition=args[2],
        right=args[4],
    )


def a(value: str) -> "Parser[Token, Token]":
    """Eq(a) -> Parser(a, a)

    Returns a parser that parses a token that is equal to the value value.
    """

    def _is_value_eq(token: Token) -> bool:
        return token.value == value

    return some(_is_value_eq).named(f'(a "{value}")')


DOT: Final = skip(a("."))
COMMA: Final = skip(a(","))
COLON: Final = skip(a(":"))

OPEN_TMPL: Final = skip(a("${{"))
CLOSE_TMPL: Final = skip(a("}}"))
OPEN_TMPL2: Final = skip(a("$[["))
CLOSE_TMPL2: Final = skip(a("]]"))

LPAR: Final = skip(a("("))
RPAR = skip(a(")"))

LSQB: Final = skip(a("["))
RSQB = skip(a("]"))

LBRACE: Final = skip(a("{"))
RBRACE = skip(a("}"))

OP_PLUS = a("+")
OP_MINUS = a("-")
OP_MUL = a("*")
OP_DIV = a("/")
OP_MOD = a("%")
OP_BITWISE_OR = a("|")
OP_CMP = a("==") | a("!=") | a("<") | a("<=") | a(">") | a(">=")
OP_NOT = a("not")
OP_OR = a("or")
OP_AND = a("and")

REAL: Final = literal("REAL") | literal("EXP")

INT: Final = literal("INT") | literal("HEX") | literal("OCT") | literal("BIN")

BOOL: Final = literal("BOOL")

STR: Final = literal("STR")

NONE: Final = literal("NONE")

LITERAL: Final = NONE | BOOL | REAL | INT | STR

NAME: Final = some(make_toktype_predicate("NAME"))

LIST_MAKER: Final = forward_decl()

DICT_MAKER: Final = forward_decl()

ATOM: Final = LITERAL | LIST_MAKER | DICT_MAKER

EXPR: Final = forward_decl()

ATOM_EXPR: Final = forward_decl()

LOOKUP_ATTR: Final = DOT + NAME >> lookup_attr

LOOKUP_ITEM: Final = LSQB + EXPR + RSQB >> lookup_item

TRAILER: Final = many(LOOKUP_ATTR | LOOKUP_ITEM)

LOOKUP: Final = NAME + TRAILER >> make_lookup

FUNC_ARGS: Final = maybe(EXPR + many(COMMA + EXPR)) >> make_args

FUNC_CALL: Final = (NAME + LPAR + FUNC_ARGS + RPAR + TRAILER) >> make_call

ATOM_EXPR.define(LPAR + EXPR + RPAR | ATOM | FUNC_CALL | LOOKUP)

# Here we define operator precedence:
# +, - (unary)
# *, /
# +, -
# |
# ==, !=, <, >, <=, =>
# and
# or

# For operators, LL1 grammar rules are used to speed-up parsing

DISJUNCTION: Final = forward_decl()
DISJUNCTION_TRAILER: Final = forward_decl()
CONJUNCTION: Final = forward_decl()
CONJUNCTION_TRAILER: Final = forward_decl()
INVERSION: Final = forward_decl()
COMPARISON: Final = forward_decl()
COMPARISON_TRAILER: Final = forward_decl()
BITWISE_OR: Final = forward_decl()
BITWISE_OR_TRAILER: Final = forward_decl()
SUM: Final = forward_decl()
SUM_TRAILER: Final = forward_decl()
TERM: Final = forward_decl()
TERM_TRAILER: Final = forward_decl()
FACTOR: Final = forward_decl()


DISJUNCTION_TRAILER.define(
    maybe(OP_OR + CONJUNCTION + DISJUNCTION_TRAILER) >> make_op_trailer
)
DISJUNCTION.define(CONJUNCTION + DISJUNCTION_TRAILER >> make_bin_op_expr)

CONJUNCTION_TRAILER.define(
    maybe(OP_AND + INVERSION + CONJUNCTION_TRAILER) >> make_op_trailer
)
CONJUNCTION.define(INVERSION + CONJUNCTION_TRAILER >> make_bin_op_expr)

INVERSION.define(OP_NOT + INVERSION >> make_unary_op_expr | COMPARISON)

COMPARISON_TRAILER.define(
    maybe(OP_CMP + BITWISE_OR + COMPARISON_TRAILER) >> make_op_trailer
)
COMPARISON.define(BITWISE_OR + COMPARISON_TRAILER >> make_bin_op_expr)

BITWISE_OR_TRAILER.define(
    maybe(OP_BITWISE_OR + SUM + BITWISE_OR_TRAILER) >> make_op_trailer
)
BITWISE_OR.define(SUM + BITWISE_OR_TRAILER >> make_bin_op_expr)

SUM_TRAILER.define(maybe((OP_PLUS | OP_MINUS) + TERM + SUM_TRAILER) >> make_op_trailer)
SUM.define(TERM + SUM_TRAILER >> make_bin_op_expr)

TERM_TRAILER.define(
    maybe((OP_MUL | OP_DIV | OP_MOD) + FACTOR + TERM_TRAILER) >> make_op_trailer
)
TERM.define(FACTOR + TERM_TRAILER >> make_bin_op_expr)

FACTOR.define((OP_PLUS | OP_MINUS) + FACTOR >> make_unary_op_expr | ATOM_EXPR)

EXPR.define(
    DISJUNCTION + a("if") + DISJUNCTION + a("else") + EXPR >> make_if_else | DISJUNCTION
)

LIST_MAKER.define(
    (LSQB + EXPR + many(COMMA + EXPR) + maybe(COMMA) + RSQB) >> make_list
    | (LSQB + EXPR + a("for") + NAME + a("in") + EXPR + RSQB) >> make_list_comp
    | (LSQB + EXPR + a("for") + NAME + a("in") + EXPR + a("if") + EXPR + RSQB)
    >> make_list_comp_with_if
    | (a("[") + a("]")) >> make_empty_list
)

DICT_MAKER.define(
    (
        LBRACE
        + EXPR
        + COLON
        + EXPR
        + many(COMMA + EXPR + COLON + EXPR)
        + maybe(COMMA)
        + RBRACE
    )
    >> make_dict  # type: ignore
    | (a("{") + a("}")) >> make_empty_dict
)

TMPL: Final = (OPEN_TMPL + EXPR + CLOSE_TMPL) | (OPEN_TMPL2 + EXPR + CLOSE_TMPL2)

TEXT: Final = some(make_toktype_predicate("TEXT")) >> make_text

PARSER: Final = oneplus(TMPL | TEXT) + skip(finished)


class BaseExpr(Generic[_T], abc.ABC):
    @abc.abstractmethod
    async def eval(self, root: RootABC) -> Optional[_T]:
        pass


IMPLICIT_STR_CONCAT: Final[Tuple[type, ...]] = (str, RemotePath, LocalPath, URL)


class Expr(BaseExpr[_T]):
    allow_none: ClassVar[bool] = True
    allow_expr: ClassVar[bool] = True
    allow_implicit_concat: ClassVar[bool] = True
    type_name: ClassVar[str]
    start: Pos
    end: Pos
    _ret: Union[None, _T]
    _pattern: Union[None, str, _T]
    _parsed: Optional[Sequence[Item]]

    @abc.abstractmethod
    def convert(self, arg: TypeT) -> _T:
        pass

    def _try_convert(self, arg: TypeT, start: Pos, end: Pos) -> None:
        try:
            self._ret = self.convert(arg)
        except (TypeError, ValueError) as exc:
            raise EvalError(str(exc), start, end)

    def __init__(self, start: Pos, end: Pos, pattern: Union[None, str, _T]) -> None:
        self.start = start
        self.end = end
        self._pattern = pattern
        # precalculated value for constant string, allows raising errors earlier
        self._ret = None
        if pattern is not None:
            if isinstance(pattern, str):
                # parse later
                pass
            else:
                # explicit non-string value is passed
                self._try_convert(pattern, start, end)
                return
            tokens = list(tokenize(pattern, start=start))
            if tokens:
                self._parsed = PARSER.parse(tokens)
                if (
                    not self.allow_implicit_concat
                    and self._parsed
                    and len(self._parsed) > 1
                ):
                    raise EvalError(
                        "Implicit concatenation is not allowed for "
                        f"{self.type_name}",
                        start,
                        end,
                    )
            else:
                if not self.allow_implicit_concat:
                    raise EvalError(
                        f"Empty value is not allowed for {self.type_name}",
                        start,
                        end,
                    )
                self._parsed = [Text(start, end, "")]
            assert self._parsed
            if len(self._parsed) == 1 and isinstance(self._parsed[0], Text):
                self._try_convert(self._parsed[0].arg, start, end)
            elif not self.allow_expr:
                raise EvalError(f"Expressions are not allowed in {pattern}", start, end)
        elif self.allow_none:
            self._parsed = None
        else:
            raise EvalError("None is not allowed", start, end)

    @property
    def pattern(self) -> Optional[str]:
        if self._pattern is None:
            return None
        return str(self._pattern)

    @property
    def value(self) -> Optional[_T]:
        if self._ret is None:
            return None
        return self._ret

    async def eval(self, root: RootABC) -> Optional[_T]:
        if self._ret is not None:
            return self._ret
        if self._parsed is not None:
            ret: List[TypeT] = []
            for part in self._parsed:
                try:
                    val = await part.eval(root)
                except asyncio.CancelledError:
                    raise
                except EvalError:
                    raise
                except Exception as exc:
                    raise EvalError(str(exc), part.start, part.end) from exc
                # TODO: add str() function, raise an explicit error if
                # an expresion evaluates non-str type
                # assert isinstance(val, str), repr(val)
                ret.append(val)
            try:
                if len(ret) == 1:
                    return self.convert(ret[0])
                else:
                    assert self.allow_implicit_concat
                    return self.convert("".join(str(item) for item in ret))
            except asyncio.CancelledError:
                raise
            except EvalError:
                raise
            except Exception as exc:
                raise EvalError(str(exc), self._parsed[0].start, self._parsed[-1].end)
        else:
            # __init__() makes sure that the pattern is not None if
            # self.allow_none is False, the check is present here
            # for better readability.
            assert self.allow_none
            return None

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({self._pattern!r})"

    def __eq__(self, other: Any) -> bool:
        if type(self) is not type(other):
            return False
        assert isinstance(other, self.__class__)
        return self._pattern == other._pattern

    def __hash__(self) -> int:
        return hash((self.__class__.__name__, self._pattern))


class StrictExpr(Expr[_T], ABC):
    allow_none = False

    async def eval(self, root: RootABC) -> _T:
        ret = await super().eval(root)
        assert ret is not None
        return ret


class NoConcatMixin:
    allow_implicit_concat = False


class NoExprMixin:
    allow_expr = False


# These comprehensive specializations exist mainly for static type checker


class PrimitiveExprMixin:
    type_name: ClassVar[str] = "primitive"

    def convert(self, arg: TypeT) -> Union[int, bool, float, str]:
        if isinstance(arg, (int, bool, float)):
            return arg
        return str(arg)


class PrimitiveExpr(PrimitiveExprMixin, StrictExpr[Union[int, bool, float, str]]):
    pass


class OptPrimitiveExpr(PrimitiveExprMixin, Expr[Union[int, bool, float, str]]):
    pass


class SimplePrimitiveExpr(
    PrimitiveExprMixin, NoExprMixin, StrictExpr[Union[int, bool, float, str]]
):
    pass


class SimpleOptPrimitiveExpr(
    PrimitiveExprMixin, NoExprMixin, Expr[Union[int, bool, float, str]]
):
    pass


class StrExprMixin:
    type_name: ClassVar[str] = "str"

    def convert(self, arg: TypeT) -> str:
        return str(arg)


class StrExpr(StrExprMixin, StrictExpr[str]):
    pass


class OptStrExpr(StrExprMixin, Expr[str]):
    pass


class SimpleStrExpr(StrExprMixin, NoExprMixin, StrictExpr[str]):
    pass


class SimpleOptStrExpr(StrExprMixin, NoExprMixin, Expr[str]):
    pass


class IdExprMixin:
    type_name: ClassVar[str] = "id"

    def convert(self, arg: TypeT) -> str:
        if not isinstance(arg, str):
            raise TypeError(f"{arg!r} is not a string")
        if not arg.isidentifier():
            raise ValueError(f"{arg!r} is not identifier")
        if arg == arg.upper():
            raise ValueError(
                f"{arg!r} is invalid identifier, "
                "uppercase names are reserved for internal usage"
            )
        return arg


class IdExpr(IdExprMixin, StrictExpr[str]):
    pass


class OptIdExpr(IdExprMixin, Expr[str]):
    pass


class SimpleIdExpr(IdExprMixin, NoExprMixin, StrictExpr[str]):
    pass


class SimpleOptIdExpr(IdExprMixin, NoExprMixin, Expr[str]):
    pass


class URIExprMixin:
    type_name: ClassVar[str] = "URL"

    def convert(self, arg: TypeT) -> URL:
        return URL(arg)  # type: ignore[arg-type]


class URIExpr(URIExprMixin, StrictExpr[URL]):
    pass


class PlatformResourceURIExpr(URIExpr):
    async def eval(self, root: RootABC) -> URL:
        ret = await super().eval(root)
        try:
            # Hack to get flow's project ctx -> project_name
            project_ctx = root.lookup("project")
        except LookupError:
            project_ctx = None

        if project_ctx:
            async with root.client() as cl:
                ret = cl.parse.str_to_uri(
                    str(ret),
                    project_name=project_ctx.project_name,  # type: ignore
                    short=True,
                )
        return ret


async def project_image_ref(img_ref: str, root: RootABC) -> str:
    project_ctx = None
    if img_ref.startswith("image:"):
        try:
            # Hack to get flow's project ctx -> project_name
            project_ctx = root.lookup("project")
        except LookupError:
            pass
    if project_ctx:
        async with root.client() as cl:
            uri = cl.parse.str_to_uri(
                img_ref,
                project_name=project_ctx.project_name,  # type: ignore
                short=True,
            )
            img_ref = str(uri)
    return img_ref


class OptImageRefStrExpr(OptStrExpr):
    async def eval(self, root: RootABC) -> Optional[str]:
        img_ref = await super().eval(root)
        if img_ref is not None:
            return await project_image_ref(img_ref, root)
        return None


class ImageRefStrExpr(StrExpr):
    async def eval(self, root: RootABC) -> str:
        img_ref = await super().eval(root)
        return await project_image_ref(img_ref, root)


class OptURIExpr(URIExprMixin, Expr[URL]):
    pass


class BoolExprMixin(NoConcatMixin):
    type_name: ClassVar[str] = "bool"

    def convert(self, arg: TypeT) -> bool:
        return bool(arg)


class BoolExpr(BoolExprMixin, StrictExpr[bool]):
    pass


class OptBoolExpr(BoolExprMixin, Expr[bool]):
    pass


class SimpleBoolExpr(BoolExprMixin, NoExprMixin, StrictExpr[bool]):
    pass


class SimpleOptBoolExpr(BoolExprMixin, NoExprMixin, Expr[bool]):
    pass


class EnableExprMixin(NoConcatMixin):
    type_name: ClassVar[str] = "enabled_type"

    def convert(self, arg: TypeT) -> Union[bool, AlwaysT]:
        if isinstance(arg, AlwaysT):
            return arg
        if arg == "always()":
            return AlwaysT()
        return bool(arg)


class EnableExpr(EnableExprMixin, StrictExpr[Union[bool, AlwaysT]]):
    pass


class OptEnableExpr(EnableExprMixin, Expr[Union[bool, AlwaysT]]):
    pass


class IntExprMixin(NoConcatMixin):
    type_name: ClassVar[str] = "int"

    def convert(self, arg: TypeT) -> int:
        return int(arg)  # type: ignore[arg-type]


class IntExpr(IntExprMixin, StrictExpr[int]):
    pass


class OptIntExpr(IntExprMixin, Expr[int]):
    pass


class FloatExprMixin(NoConcatMixin):
    type_name: ClassVar[str] = "float"

    def convert(self, arg: TypeT) -> float:
        return float(arg)  # type: ignore[arg-type]


class FloatExpr(FloatExprMixin, StrictExpr[float]):
    pass


class OptFloatExpr(FloatExprMixin, Expr[float]):
    pass


class OptTimeDeltaExpr(OptFloatExpr):
    type_name: ClassVar[str] = "timedelta"
    RE = re.compile(r"^((?P<d>\d+)d)?((?P<h>\d+)h)?((?P<m>\d+)m)?((?P<s>\d+)s)?$")

    def convert(self, arg: TypeT) -> float:
        try:
            return super().convert(arg)
        except (ValueError, SyntaxError):
            assert isinstance(arg, str)
            match = self.RE.match(arg)
            if match is None:
                raise ValueError(f"{arg!r} is not a time delta unit")
            td = datetime.timedelta(
                days=int(match.group("d") or 0),
                hours=int(match.group("h") or 0),
                minutes=int(match.group("m") or 0),
                seconds=int(match.group("s") or 0),
            )
            return td.total_seconds()


class LocalPathMixin:
    type_name: ClassVar[str] = "LocalPath"

    def convert(self, arg: TypeT) -> LocalPath:
        return LocalPath(arg)  # type: ignore[arg-type]


class LocalPathExpr(LocalPathMixin, StrictExpr[LocalPath]):
    pass


class OptLocalPathExpr(LocalPathMixin, Expr[LocalPath]):
    pass


class RemotePathMixin:
    type_name: ClassVar[str] = "RemotePath"

    def convert(self, arg: TypeT) -> RemotePath:
        return RemotePath(arg)  # type: ignore[arg-type]


class RemotePathExpr(RemotePathMixin, StrictExpr[RemotePath]):
    pass


class OptRemotePathExpr(RemotePathMixin, Expr[RemotePath]):
    pass


class OptBashExpr(OptStrExpr):
    def convert(self, arg: TypeT) -> str:
        ret = " ".join(["bash", "-euo", "pipefail", "-c", shlex.quote(str(arg))])
        return ret


class OptPythonExpr(OptStrExpr):
    def convert(self, arg: TypeT) -> str:
        ret = " ".join(["python3", "-uc", shlex.quote(str(arg))])
        return ret


PORT_PAIR_RE = re.compile(r"^\d+:\d+$")


def port_pair_item(arg: TypeT) -> str:
    sarg = str(arg)
    match = PORT_PAIR_RE.match(sarg)
    if match is None:
        raise ValueError(f"{arg!r} is not a LOCAL:REMOTE ports pair")
    return sarg


class PortPairExpr(StrExpr):
    type_name: ClassVar[str] = "PortPair"

    def convert(self, arg: TypeT) -> str:
        return port_pair_item(arg)


class BaseSequenceExpr(BaseExpr[SequenceT], abc.ABC):
    pass


class ConcatSequenceExpr(BaseSequenceExpr):
    def __init__(self, *seqs: BaseSequenceExpr):
        self._seqs = seqs

    async def eval(self, root: RootABC) -> SequenceT:
        ret: List[TypeT] = []
        for seq in self._seqs:
            value = await seq.eval(root)
            if value:
                ret.extend(value)
        return cast(SequenceT, ret)


class SequenceExpr(BaseSequenceExpr, NoConcatMixin, Expr[SequenceT]):
    type_name: ClassVar[str] = "Sequence"

    def __init__(
        self,
        start: Pos,
        end: Pos,
        pattern: Union[None, str, SequenceT],
        item_factory: Callable[[TypeT], TypeT],
    ) -> None:
        super().__init__(start, end, pattern)
        self._item_factory = item_factory

    def convert(self, arg: TypeT) -> SequenceT:
        if not isinstance(arg, SequenceT):
            raise TypeError(f"{arg!r} is not a sequence")
        ret: List[TypeT] = []
        for item in arg:
            ret.append(self._item_factory(item))
        return cast(SequenceT, ret)


class SequenceItemsExpr(BaseSequenceExpr, Generic[_IT]):
    def __init__(self, items: Sequence[Expr[_IT]]) -> None:
        self._items = items

    async def eval(self, root: RootABC) -> SequenceT:
        ret = []
        for item in self._items:
            ret.append(await item.eval(root))
        return cast(SequenceT, ret)

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({self._items!r})"

    def __eq__(self, other: Any) -> bool:
        if type(self) is not type(other):
            return False
        assert isinstance(other, self.__class__)
        return self._items == other._items

    def __hash__(self) -> int:
        return hash((self.__class__.__name__, self._items))


class BaseMappingExpr(BaseExpr[MappingT]):
    pass


class MergeMappingsExpr(BaseMappingExpr):
    def __init__(self, *mappings: BaseMappingExpr):
        self._mappings = mappings

    async def eval(self, root: RootABC) -> MappingT:
        ret = {}
        for mapping in reversed(self._mappings):
            value = await mapping.eval(root)
            if value:
                for key in value:
                    ret[key] = value[key]
        return cast(MappingT, ret)


class MappingExpr(BaseMappingExpr, NoConcatMixin, StrictExpr[MappingT]):
    type_name: ClassVar[str] = "Mapping"

    def __init__(
        self,
        start: Pos,
        end: Pos,
        pattern: Union[None, str, MappingT],
        value_factory: Callable[[TypeT], TypeT],
    ) -> None:
        super().__init__(start, end, pattern)
        self._value_factory = value_factory

    def convert(self, arg: TypeT) -> MappingT:
        if not isinstance(arg, MappingT):
            raise TypeError(f"{arg!r} is not a sequence")
        ret = {}
        for key, value in arg.items():  # type: ignore[attr-defined]
            if not isinstance(key, str):
                raise TypeError(f"{key:r} is not a string")
            ret[key] = self._value_factory(value)
        return cast(MappingT, ret)


class MappingItemsExpr(BaseMappingExpr, Generic[_IT]):
    def __init__(self, items: Mapping[str, Expr[_IT]]) -> None:
        self._items = items

    async def eval(self, root: RootABC) -> MappingT:
        ret = {}
        for key, value in self._items.items():
            ret[key] = await value.eval(root)
        return cast(MappingT, ret)

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({self._items!r})"

    def __eq__(self, other: Any) -> bool:
        if type(self) is not type(other):
            return False
        assert isinstance(other, self.__class__)
        return self._items == other._items

    def __hash__(self) -> int:
        return hash((self.__class__.__name__, self._items))


def restart_policy_item(arg: TypeT) -> str:
    sarg = str(arg)
    try:
        arg = JobRestartPolicy(sarg)
    except ValueError:
        allowed_values = ", ".join(list(JobRestartPolicy))
        raise ValueError(
            f"{arg!r} is not a valid restart policy, allowed: {allowed_values}"
        )
    return arg


class OptRestartPolicyExpr(OptStrExpr):
    type_name: ClassVar[str] = "RestartPolicy"

    def convert(self, arg: TypeT) -> str:
        return restart_policy_item(arg)
