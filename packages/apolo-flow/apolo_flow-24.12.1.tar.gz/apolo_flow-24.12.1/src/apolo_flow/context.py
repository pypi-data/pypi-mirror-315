import dataclasses
from dataclasses import dataclass, fields, replace

import collections
import enum
import hashlib
import itertools
import json
import logging
import re
import shlex
from abc import ABC, abstractmethod
from apolo_sdk import Client
from contextlib import asynccontextmanager
from datetime import timedelta
from functools import lru_cache
from typing import (
    AbstractSet,
    Any,
    AsyncIterator,
    Dict,
    Generic,
    Iterable,
    List,
    Mapping,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)
from typing_extensions import Annotated, Protocol
from yarl import URL

from apolo_flow import ast
from apolo_flow.ast import InputType
from apolo_flow.colored_topo_sorter import ColoredTopoSorter
from apolo_flow.config_loader import ActionSpec, ConfigLoader
from apolo_flow.expr import (
    BaseMappingExpr,
    BaseSequenceExpr,
    ConcatSequenceExpr,
    EnableExpr,
    EvalError,
    Expr,
    IdExpr,
    LiteralT,
    MergeMappingsExpr,
    OptStrExpr,
    RootABC,
    StrExpr,
    TypeT,
)
from apolo_flow.types import AlwaysT, FullID, GitInfo, LocalPath, RemotePath, TaskStatus
from apolo_flow.utils import collect_git_info


log = logging.getLogger(__name__)


# Exceptions


class NotAvailable(LookupError):
    def __init__(self, ctx_name: str) -> None:
        super().__init__(f"The '{ctx_name}' context is not available")


class UnknownJob(KeyError):
    pass


class UnknownTask(KeyError):
    pass


PROJECT_ROLE_DEPRECATED_MSG = (
    "Flow roles are deprecated and will be ignored. "
    "To grant access to the flow and its artifacts, please add users "
    "to the corresponding project using `apolo admin add-project-user`."
)

# ...Ctx types, they define parts that can be available in expressions


EnvCtx = Annotated[Mapping[str, str], "EnvCtx"]
TagsCtx = Annotated[AbstractSet[str], "TagsCtx"]
VolumesCtx = Annotated[Mapping[str, "VolumeCtx"], "VolumesCtx"]
ImagesCtx = Annotated[Mapping[str, "ImageCtx"], "ImagesCtx"]
InputsCtx = Annotated[Mapping[str, Union[int, float, bool, str]], "InputsCtx"]
ParamsCtx = Annotated[Mapping[str, str], "ParamsCtx"]

NeedsCtx = Annotated[Mapping[str, "DepCtx"], "NeedsCtx"]
StateCtx = Annotated[Mapping[str, str], "StateCtx"]
MatrixCtx = Annotated[Mapping[str, LiteralT], "MatrixCtx"]


@dataclass(frozen=True)
class ProjectCtx:
    id: str
    project_name: str
    owner: Optional[str] = None
    role: Optional[str] = None


@dataclass(frozen=True)
class FlowCtx:
    flow_id: str
    project_id: str
    workspace: LocalPath
    title: str
    username: str

    @property
    def id(self) -> str:
        # TODO: add a custom warning API to report with config file name and
        # line numbers instead of bare printing
        import click

        click.echo(
            click.style(
                "flow.id attribute is deprecated, use flow.flow_id instead", fg="yellow"
            )
        )
        return self.flow_id

    def with_action(self, action_path: LocalPath) -> "ActionFlowCtx":
        # action_path can be not None if an action is called from another action
        return ActionFlowCtx(
            flow_id=self.flow_id,
            project_id=self.project_id,
            workspace=self.workspace,
            title=self.title,
            username=self.username,
            action_path=action_path,
        )


@dataclass(frozen=True)
class BatchFlowCtx(FlowCtx):
    life_span: Optional[float]


@dataclass(frozen=True)
class ActionFlowCtx(FlowCtx):
    action_path: LocalPath


@dataclass(frozen=True)
class VolumeCtx:
    id: str
    remote: URL
    mount: RemotePath
    read_only: bool
    local: Optional[LocalPath]
    full_local_path: Optional[LocalPath]

    @property
    def ref_ro(self) -> str:
        return f"{self.remote}:{self.mount}:ro"

    @property
    def ref_rw(self) -> str:
        return f"{self.remote}:{self.mount}:rw"

    @property
    def ref(self) -> str:
        ro = "ro" if self.read_only else "rw"
        return f"{self.remote}:{self.mount}:{ro}"


@dataclass(frozen=True)
class EarlyImageCtx:
    id: str
    ref: str
    context: Optional[Union[URL, LocalPath]]
    dockerfile: Optional[Union[URL, LocalPath]]
    dockerfile_rel: Optional[Union[LocalPath, RemotePath]]

    def to_image_ctx(
        self,
        build_args: Sequence[str],
        env: Mapping[str, str],
        volumes: Sequence[str],
        build_preset: Optional[str],
        force_rebuild: bool,
        extra_kaniko_args: Optional[str],
    ) -> "ImageCtx":
        return ImageCtx(
            id=self.id,
            ref=self.ref,
            context=self.context,
            dockerfile=self.dockerfile,
            dockerfile_rel=self.dockerfile_rel,
            build_args=build_args,
            env=env,
            volumes=volumes,
            build_preset=build_preset,
            force_rebuild=force_rebuild,
            extra_kaniko_args=extra_kaniko_args,
        )

    def get_ctx_storage_dir(self, project_name: str, project_id: str) -> URL:
        img_part = self.ref.replace(":", "/")
        while "//" in img_part:
            img_part = img_part.replace("//", "/")
        return URL(f"storage:/{project_name}/.flow/{project_id}/{img_part}")


@dataclass(frozen=True)
class ImageCtx(EarlyImageCtx):
    build_args: Sequence[str]
    env: Mapping[str, str]
    volumes: Sequence[str]
    build_preset: Optional[str]
    force_rebuild: bool
    extra_kaniko_args: Optional[str]


@dataclass(frozen=True)
class MultiCtx:
    args: str
    suffix: str


@dataclass(frozen=True)
class StrategyCtx:
    fail_fast: bool = True
    max_parallel: int = 10


@dataclass(frozen=True)
class DepCtx:
    result: TaskStatus
    outputs: Mapping[str, str]

    def __post_init__(self) -> None:
        assert (
            self.result != TaskStatus.CACHED
        ), "CACHED status should replaced with SUCCEEDED for expressions"


@dataclass(frozen=True)
class GitCtx:
    _git_info: Optional[GitInfo]

    def _get_info(self) -> GitInfo:
        if not self._git_info:
            raise ValueError("Git info is not available: is this project under git?")
        return self._git_info

    @property
    def sha(self) -> str:
        return self._get_info().sha

    @property
    def branch(self) -> str:
        return self._get_info().branch

    @property
    def tags(self) -> Sequence[str]:
        return self._get_info().tags


# Confs (similar to ..Ctx, but not available to expressions, only used
# during evaluation)


@dataclass(frozen=True)
class CacheConf:
    strategy: ast.CacheStrategy = ast.CacheStrategy.DEFAULT
    life_span: float = 14 * 24 * 3600


@dataclass(frozen=True)
class DefaultsConf:
    volumes: Sequence[str] = ()
    workdir: Optional[RemotePath] = None
    life_span: Optional[float] = None
    schedule_timeout: Optional[float] = None
    preset: Optional[str] = None


# Return dataclasses
# Returned by flow classes to provide data to runner/executor.


@dataclass(frozen=True)
class ExecUnit:
    title: Optional[str]
    name: Optional[str]
    image: str
    preset: Optional[str]
    schedule_timeout: Optional[float]
    http_port: Optional[int]
    http_auth: Optional[bool]
    pass_config: Optional[bool]
    entrypoint: Optional[str]
    cmd: Optional[str]
    workdir: Optional[RemotePath]
    volumes: Sequence[str]  # Sequence[VolumeRef]
    life_span: Optional[float]
    env: Mapping[str, str]
    tags: AbstractSet[str]
    restart: Optional[str]


@dataclass(frozen=True)
class Job(ExecUnit):
    id: str
    detach: bool
    browse: bool
    port_forward: Sequence[str]
    multi: bool


@dataclass(frozen=True)
class Task(ExecUnit):
    # executed task
    id: Optional[str]

    # continue_on_error: Optional[bool]
    enable: Union[bool, AlwaysT]

    strategy: StrategyCtx
    cache: "CacheConf"

    caching_key: str


@dataclass(frozen=True)
class LocalTask:
    # executed task
    id: Optional[str]
    cmd: str


@dataclass(frozen=True)
class TaskMeta:
    enable: Union[bool, AlwaysT]

    strategy: StrategyCtx
    cache: "CacheConf"


@dataclass(frozen=True)
class JobMeta:
    # Metadata used for jobs lookup
    id: str
    multi: bool
    tags: AbstractSet[str]


@dataclass(frozen=True)
class LocallyPreparedInfo:
    """Tree-like structure that stores locally prepared info for a the batch flow."""

    children_info: Mapping[str, "LocallyPreparedInfo"]

    git_info: Optional[GitInfo]
    early_images: Mapping[str, EarlyImageCtx]


# ...Context classes, used to complete container of what is available
# to expressions


class EmptyRoot(RootABC):
    def lookup(self, name: str) -> TypeT:
        raise NotAvailable(name)

    @asynccontextmanager
    async def client(self) -> AsyncIterator[Client]:
        raise RuntimeError("apolo API is not available in <empty> context")
        yield Client()  # fake lint to make the code a real async iterator

    @property
    def dry_run(self) -> bool:
        return False


EMPTY_ROOT = EmptyRoot()


@dataclass(frozen=True)
class Context(RootABC):
    _client: Client
    _dry_run: bool

    def lookup(self, name: str) -> TypeT:
        for f in fields(self):
            if f.name != name:
                continue
            break
        else:
            raise NotAvailable(name)
        ret = getattr(self, name)
        # assert isinstance(ret, (ContainerT, SequenceT, MappingT)), ret
        return cast(TypeT, ret)

    @asynccontextmanager
    async def client(self) -> AsyncIterator[Client]:
        yield self._client

    @property
    def dry_run(self) -> bool:
        return self._dry_run


_MODULE_PARENT = TypeVar("_MODULE_PARENT", bound=RootABC)


@dataclass(frozen=True)
class ModuleContext(Context, Generic[_MODULE_PARENT]):
    _parent: _MODULE_PARENT

    def lookup(self, name: str) -> TypeT:
        try:
            return super().lookup(name)
        except NotAvailable:
            return self._parent.lookup(name)


_FLOW_CTX = TypeVar("_FLOW_CTX", bound=FlowCtx)


@dataclass(frozen=True)
class WithFlowContext(Context, Generic[_FLOW_CTX]):
    project: ProjectCtx
    flow: _FLOW_CTX


@dataclass(frozen=True)
class WithEnvContext(Context):
    env: EnvCtx


@dataclass(frozen=True)
class LiveContextStep1(WithFlowContext[FlowCtx], Context):
    git: GitCtx

    def to_live_ctx(
        self, env: EnvCtx, tags: TagsCtx, volumes: VolumesCtx, images: ImagesCtx
    ) -> "LiveContext":
        return LiveContext(
            project=self.project,
            flow=self.flow,
            git=self.git,
            env=env,
            tags=tags,
            volumes=volumes,
            images=images,
            _client=self._client,
            _dry_run=self._dry_run,
        )


@dataclass(frozen=True)
class LiveContext(WithEnvContext, LiveContextStep1):
    tags: TagsCtx
    volumes: VolumesCtx
    images: ImagesCtx

    def to_job_ctx(self, params: ParamsCtx) -> "LiveJobContext":
        return LiveJobContext(
            project=self.project,
            flow=self.flow,
            git=self.git,
            env=self.env,
            tags=self.tags,
            volumes=self.volumes,
            images=self.images,
            params=params,
            _client=self._client,
            _dry_run=self._dry_run,
        )

    def to_multi_job_ctx(
        self, multi: MultiCtx, params: ParamsCtx
    ) -> "LiveMultiJobContext":
        return LiveMultiJobContext(
            project=self.project,
            flow=self.flow,
            git=self.git,
            env=self.env,
            tags=self.tags,
            volumes=self.volumes,
            images=self.images,
            multi=multi,
            params=params,
            _client=self._client,
            _dry_run=self._dry_run,
        )


@dataclass(frozen=True)
class LiveJobContext(LiveContext):
    params: ParamsCtx


@dataclass(frozen=True)
class LiveMultiJobContext(LiveContext):
    multi: MultiCtx
    params: ParamsCtx


@dataclass(frozen=True)
class LiveActionContext(Context):
    inputs: InputsCtx
    flow: ActionFlowCtx


@dataclass(frozen=True)
class LiveModuleContext(ModuleContext[_MODULE_PARENT]):
    inputs: InputsCtx


@dataclass(frozen=True)
class BatchContextStep1(WithFlowContext[BatchFlowCtx], Context):
    params: ParamsCtx
    git: GitCtx

    def to_step_2(
        self, env: EnvCtx, tags: TagsCtx, volumes: VolumesCtx, images: ImagesCtx
    ) -> "BatchContextStep2":
        return BatchContextStep2(
            project=self.project,
            flow=self.flow,
            params=self.params,
            git=self.git,
            env=env,
            tags=tags,
            volumes=volumes,
            images=images,
            _client=self._client,
            _dry_run=self._dry_run,
        )


@dataclass(frozen=True)
class BatchContextStep2(WithEnvContext, BatchContextStep1):
    tags: TagsCtx
    volumes: VolumesCtx
    images: ImagesCtx

    def to_batch_ctx(
        self,
        strategy: StrategyCtx,
    ) -> "BatchContext":
        return BatchContext(
            project=self.project,
            flow=self.flow,
            params=self.params,
            git=self.git,
            env=self.env,
            tags=self.tags,
            volumes=self.volumes,
            images=self.images,
            strategy=strategy,
            _client=self._client,
            _dry_run=self._dry_run,
        )


class BaseBatchContext(Context):
    strategy: StrategyCtx
    images: ImagesCtx

    @abstractmethod
    def to_matrix_ctx(
        self, strategy: StrategyCtx, matrix: MatrixCtx
    ) -> "BaseMatrixContext":
        pass


class BaseMatrixContext(BaseBatchContext):
    matrix: MatrixCtx

    @abstractmethod
    def to_task_ctx(self, needs: NeedsCtx, state: StateCtx) -> "BaseTaskContext":
        pass


@dataclass(frozen=True)
class MatrixOnlyContext(Context):
    matrix: MatrixCtx


class BaseTaskContext(BaseMatrixContext):
    strategy: StrategyCtx
    needs: NeedsCtx
    state: StateCtx


@dataclass(frozen=True)
class BatchContext(BaseBatchContext, BatchContextStep2):
    strategy: StrategyCtx

    def to_matrix_ctx(
        self, strategy: StrategyCtx, matrix: MatrixCtx
    ) -> "BatchMatrixContext":
        return BatchMatrixContext(
            project=self.project,
            flow=self.flow,
            params=self.params,
            git=self.git,
            env=self.env,
            tags=self.tags,
            volumes=self.volumes,
            images=self.images,
            strategy=strategy,
            matrix=matrix,
            _client=self._client,
            _dry_run=self._dry_run,
        )


@dataclass(frozen=True)
class BatchMatrixContext(BaseMatrixContext, BatchContext):
    matrix: MatrixCtx

    def to_task_ctx(self, needs: NeedsCtx, state: StateCtx) -> "BatchTaskContext":
        return BatchTaskContext(
            project=self.project,
            flow=self.flow,
            params=self.params,
            git=self.git,
            env=self.env,
            tags=self.tags,
            volumes=self.volumes,
            images=self.images,
            strategy=self.strategy,
            matrix=self.matrix,
            needs=needs,
            state=state,
            _client=self._client,
            _dry_run=self._dry_run,
        )


@dataclass(frozen=True)
class BatchTaskContext(BaseTaskContext, BatchMatrixContext):
    needs: NeedsCtx
    state: StateCtx


@dataclass(frozen=True)
class BatchActionContextStep1(ModuleContext[_MODULE_PARENT]):
    inputs: InputsCtx
    strategy: StrategyCtx
    git: GitCtx
    flow: ActionFlowCtx

    def to_action_ctx(self, images: ImagesCtx) -> "BatchActionContext[_MODULE_PARENT]":
        return BatchActionContext(
            flow=self.flow,
            git=self.git,
            images=images,
            inputs=self.inputs,
            strategy=self.strategy,
            _client=self._client,
            _dry_run=self._dry_run,
            _parent=self._parent,
        )


@dataclass(frozen=True)
class BatchActionContext(BatchActionContextStep1[_MODULE_PARENT], BaseBatchContext):
    images: ImagesCtx

    def to_matrix_ctx(
        self, strategy: StrategyCtx, matrix: MatrixCtx
    ) -> "BatchActionMatrixContext[_MODULE_PARENT]":
        return BatchActionMatrixContext(
            flow=self.flow,
            git=self.git,
            inputs=self.inputs,
            images=self.images,
            matrix=matrix,
            strategy=strategy,
            _client=self._client,
            _dry_run=self._dry_run,
            _parent=self._parent,
        )

    def to_outputs_ctx(
        self, needs: NeedsCtx
    ) -> "BatchActionOutputsContext[_MODULE_PARENT]":
        return BatchActionOutputsContext(
            flow=self.flow,
            git=self.git,
            images=self.images,
            inputs=self.inputs,
            needs=needs,
            strategy=self.strategy,
            _client=self._client,
            _dry_run=self._dry_run,
            _parent=self._parent,
        )


@dataclass(frozen=True)
class BatchActionOutputsContext(BatchActionContext[_MODULE_PARENT]):
    needs: NeedsCtx


@dataclass(frozen=True)
class BatchActionMatrixContext(BaseMatrixContext, BatchActionContext[_MODULE_PARENT]):
    matrix: MatrixCtx
    strategy: StrategyCtx

    def to_task_ctx(
        self, needs: NeedsCtx, state: StateCtx
    ) -> "BatchActionTaskContext[_MODULE_PARENT]":
        return BatchActionTaskContext(
            flow=self.flow,
            git=self.git,
            images=self.images,
            inputs=self.inputs,
            matrix=self.matrix,
            needs=needs,
            state=state,
            strategy=self.strategy,
            _client=self._client,
            _dry_run=self._dry_run,
            _parent=self._parent,
        )


@dataclass(frozen=True)
class BatchActionTaskContext(BaseTaskContext, BatchActionMatrixContext[_MODULE_PARENT]):
    needs: NeedsCtx
    state: StateCtx


@dataclass(frozen=True)
class StatefulActionContext(Context):
    inputs: InputsCtx


@dataclass(frozen=True)
class LocalActionContext(Context):
    inputs: InputsCtx


def sanitize_name(name: str) -> str:
    # replace non-printable characters with "_"
    if not name.isprintable():
        name = "".join(c if c.isprintable() else "_" for c in name)
    # ":" is special in role name, replace it with "_"
    name = name.replace(":", "_")
    name = name.replace(" ", "_")  # replace space for readability
    name = re.sub(r"//+", "/", name)  # collapse repeated "/"
    name = name.strip("/")  # remove initial and and trailing "/"
    name = name or "_"  # name should be non-empty
    return name


async def setup_project_ctx(
    ctx: RootABC,
    config_loader: ConfigLoader,
) -> ProjectCtx:
    ast_project = await config_loader.fetch_project()
    project_id = await ast_project.id.eval(ctx)
    project_name = await ast_project.project_name.eval(ctx)
    # TODO (y.s.): Should we deprecate project_owner?
    project_owner = await ast_project.owner.eval(ctx)
    project_role = await ast_project.role.eval(ctx)
    if project_role:
        log.warning(PROJECT_ROLE_DEPRECATED_MSG)
    project_role = None
    if not project_name:
        project_name = config_loader.client.config.project_name_or_raise
    return ProjectCtx(
        id=project_id, owner=project_owner, role=project_role, project_name=project_name
    )


async def setup_flow_ctx(
    ctx: RootABC,
    ast_flow: ast.BaseFlow,
    config_name: str,
    config_loader: ConfigLoader,
    project: ProjectCtx,
) -> FlowCtx:
    flow_id = await ast_flow.id.eval(ctx)
    if flow_id is None:
        flow_id = config_name.replace("-", "_")
    flow_title = await ast_flow.title.eval(ctx)

    return FlowCtx(
        flow_id=flow_id,
        project_id=project.id,
        workspace=config_loader.workspace,
        title=flow_title or flow_id,
        username=config_loader.client.config.username,
    )


async def setup_batch_flow_ctx(
    ctx: RootABC,
    ast_flow: ast.BatchFlow,
    config_name: str,
    config_loader: ConfigLoader,
    project: ProjectCtx,
) -> BatchFlowCtx:
    base_flow = await setup_flow_ctx(ctx, ast_flow, config_name, config_loader, project)
    life_span = await ast_flow.life_span.eval(ctx)
    return BatchFlowCtx(
        flow_id=base_flow.flow_id,
        project_id=base_flow.project_id,
        workspace=base_flow.workspace,
        title=base_flow.title,
        username=config_loader.client.config.username,
        life_span=life_span,
    )


async def setup_defaults_env_tags_ctx(
    ctx: WithFlowContext[_FLOW_CTX],
    ast_defaults: Optional[ast.FlowDefaults],
    ast_global_defaults: Optional[ast.FlowDefaults],
) -> Tuple[DefaultsConf, EnvCtx, TagsCtx]:
    if ast_defaults is not None and ast_global_defaults is not None:
        ast_defaults = await merge_asts(ast_defaults, ast_global_defaults)
    elif ast_global_defaults:
        ast_defaults = ast_global_defaults
    env: EnvCtx
    tags: TagsCtx
    volumes: List[str]
    if ast_defaults is not None:
        if ast_defaults.env is not None:
            tmp_env = await ast_defaults.env.eval(ctx)
            assert isinstance(tmp_env, dict)
            env = tmp_env
        else:
            env = {}

        if ast_defaults.tags is not None:
            tmp_tags = await ast_defaults.tags.eval(ctx)
            assert isinstance(tmp_tags, list)
            tags = set(tmp_tags)
        else:
            tags = set()

        if ast_defaults.volumes:
            tmp_volumes = await ast_defaults.volumes.eval(ctx)
            assert isinstance(tmp_volumes, list)
            volumes = []
            for volume in tmp_volumes:
                if volume:
                    volumes.append(volume)
        else:
            volumes = []
        workdir = await ast_defaults.workdir.eval(ctx)
        life_span = await ast_defaults.life_span.eval(ctx)
        preset = await ast_defaults.preset.eval(ctx)
        schedule_timeout = await ast_defaults.schedule_timeout.eval(ctx)
    else:
        env = {}
        tags = set()
        volumes = []
        workdir = None
        life_span = None
        preset = None
        schedule_timeout = None

    tags.add(f"project:{_id2tag(ctx.flow.project_id)}")
    tags.add(f"flow:{_id2tag(ctx.flow.flow_id)}")

    defaults = DefaultsConf(
        volumes=volumes,
        workdir=workdir,
        life_span=life_span,
        preset=preset,
        schedule_timeout=schedule_timeout,
    )
    return defaults, env, tags


def _calc_full_path(
    ctx: WithFlowContext[_FLOW_CTX], path: Optional[LocalPath]
) -> Optional[LocalPath]:
    if path is None:
        return None
    if path.is_absolute():
        return path
    return ctx.flow.workspace.joinpath(path).resolve()


async def setup_volumes_ctx(
    ctx: WithFlowContext[_FLOW_CTX],
    ast_volumes: Optional[Mapping[str, ast.Volume]],
) -> VolumesCtx:
    volumes = {}
    if ast_volumes is not None:
        for k, v in ast_volumes.items():
            local_path = await v.local.eval(ctx)
            volumes[k] = VolumeCtx(
                id=k,
                remote=await v.remote.eval(ctx),
                mount=await v.mount.eval(ctx),
                read_only=bool(await v.read_only.eval(ctx)),
                local=local_path,
                full_local_path=_calc_full_path(ctx, local_path),
            )
    return volumes


async def setup_local_or_storage_path(
    str_expr: OptStrExpr,
    ctx: RootABC,
    flow_ctx: WithFlowContext[_FLOW_CTX],
) -> Optional[Union[URL, LocalPath]]:
    path_str = await str_expr.eval(ctx)
    if path_str is None:
        return None
    async with ctx.client() as client:
        if path_str.startswith("storage"):
            try:
                return client.parse.str_to_uri(path_str)
            except ValueError as e:
                raise EvalError(str(e), str_expr.start, str_expr.end)
    try:
        path = LocalPath(path_str)
    except ValueError as e:
        raise EvalError(str(e), str_expr.start, str_expr.end)
    return _calc_full_path(flow_ctx, path)


def _get_dockerfile_rel(
    image: ast.Image,
    context: Optional[Union[LocalPath, URL]],
    dockerfile: Optional[Union[LocalPath, URL]],
) -> Optional[Union[LocalPath, RemotePath]]:
    if context is None and dockerfile is None:
        return None
    if context is None or dockerfile is None:
        raise EvalError(
            "Partially defined image: either both context and "
            "dockerfile should be set or not set",
            image._start,
            image._end,
        )
    if isinstance(context, LocalPath) and isinstance(dockerfile, LocalPath):
        try:
            return dockerfile.relative_to(context)
        except ValueError as e:
            raise EvalError(str(e), image.dockerfile.start, image.dockerfile.end)
    elif isinstance(context, URL) and isinstance(dockerfile, URL):
        try:
            return RemotePath(dockerfile.path).relative_to(RemotePath(context.path))
        except ValueError as e:
            raise EvalError(str(e), image.dockerfile.start, image.dockerfile.end)
    else:
        raise EvalError(
            "Mixed local/storage context is not supported: "
            f"context is "
            f"{'local' if isinstance(context, LocalPath) else 'on storage'},"  # noqa: E501
            f" but dockerfile is "
            f"{'local' if isinstance(dockerfile, LocalPath) else 'on storage'}",  # noqa: E501
            image._start,
            image._end,
        )


async def setup_images_early(
    ctx: RootABC,
    flow_ctx: WithFlowContext[_FLOW_CTX],
    ast_images: Optional[Mapping[str, ast.Image]],
) -> Mapping[str, EarlyImageCtx]:
    images = {}
    if ast_images is not None:
        for k, i in ast_images.items():
            try:
                context = await setup_local_or_storage_path(i.context, ctx, flow_ctx)
                dockerfile = await setup_local_or_storage_path(
                    i.dockerfile, ctx, flow_ctx
                )
            except EvalError as e:
                # During early evaluation, some contexts maybe be missing
                if not isinstance(e.__cause__, NotAvailable):
                    raise
                context = dockerfile = None
            dockerfile_rel = _get_dockerfile_rel(i, context, dockerfile)

            images[k] = EarlyImageCtx(
                id=k,
                ref=await i.ref.eval(ctx),
                context=context,
                dockerfile=dockerfile,
                dockerfile_rel=dockerfile_rel,
            )
    return images


async def setup_images_ctx(
    ctx: RootABC,
    flow_ctx: WithFlowContext[_FLOW_CTX],
    ast_images: Optional[Mapping[str, ast.Image]],
    early_images: Optional[Mapping[str, EarlyImageCtx]] = None,
) -> ImagesCtx:
    early_images = early_images or await setup_images_early(ctx, flow_ctx, ast_images)
    assert early_images is not None
    images = {}
    if ast_images is not None:
        for k, i in ast_images.items():
            build_args: List[str] = []
            if i.build_args is not None:
                tmp_build_args = await i.build_args.eval(ctx)
                assert isinstance(tmp_build_args, list)
                build_args = tmp_build_args

            image_env: Dict[str, str] = {}
            if i.env is not None:
                tmp_env = await i.env.eval(ctx)
                assert isinstance(tmp_env, dict)
                image_env.update(tmp_env)

            image_volumes: List[str] = []
            if i.volumes is not None:
                tmp_volumes = await i.volumes.eval(ctx)
                assert isinstance(tmp_volumes, list)
                for volume in tmp_volumes:
                    if volume:
                        image_volumes.append(volume)

            image_ctx = early_images[k].to_image_ctx(
                build_args=build_args,
                env=image_env,
                volumes=image_volumes,
                build_preset=await i.build_preset.eval(ctx),
                force_rebuild=await i.force_rebuild.eval(ctx) or False,
                extra_kaniko_args=await i.extra_kaniko_args.eval(ctx),
            )
            if image_ctx.context is None:  # if true, dockerfile is None also
                # Context was not computed during early evaluation,
                # either it is missing at all or it uses non-locally
                # available context. It is safe to recompute it.
                context = await setup_local_or_storage_path(i.context, ctx, flow_ctx)
                dockerfile = await setup_local_or_storage_path(
                    i.dockerfile, ctx, flow_ctx
                )
                dockerfile_rel = _get_dockerfile_rel(i, context, dockerfile)
                image_ctx = replace(
                    image_ctx,
                    context=context,
                    dockerfile=dockerfile,
                    dockerfile_rel=dockerfile_rel,
                )
            images[k] = image_ctx
    return images


async def validate_action_call(
    call_ast: Union[ast.BaseActionCall, ast.BaseModuleCall],
    ast_inputs: Optional[Mapping[str, ast.Input]],
) -> None:
    supported_inputs: Set[str]
    supplied_inputs: Set[str]
    if ast_inputs:
        supported_inputs = set(ast_inputs.keys())
        required_inputs = {
            input_name
            for input_name, input_ast in ast_inputs.items()
            if input_ast.default.pattern is None
        }
    else:
        supported_inputs = set()
        required_inputs = set()
    if call_ast.args:
        supplied_inputs = set(call_ast.args.keys())
    else:
        supplied_inputs = set()
    missing = required_inputs - supplied_inputs
    if missing:
        raise EvalError(
            f"Required input(s): {','.join(sorted(missing))}",
            call_ast._start,
            call_ast._end,
        )
    extra = supplied_inputs - supported_inputs
    if extra:
        raise EvalError(
            f"Unsupported input(s): {','.join(sorted(extra))}",
            call_ast._start,
            call_ast._end,
        )


async def setup_inputs_ctx(
    ctx: RootABC,
    call_ast: Union[ast.BaseActionCall, ast.BaseModuleCall],
    ast_inputs: Optional[Mapping[str, ast.Input]],
) -> InputsCtx:
    await validate_action_call(call_ast, ast_inputs)
    if call_ast.args is None or ast_inputs is None:
        return {}
    inputs = {k: await v.eval(ctx) for k, v in call_ast.args.items()}
    for key, value in inputs.copy().items():
        input_ast = ast_inputs[key]
        arg_ast = call_ast.args[key]
        if input_ast.type == InputType.STR:
            if not isinstance(value, str):
                eval_error = EvalError(
                    f"Implicit casting of action argument '{key}' to string"
                    f" is deprecated",
                    arg_ast.start,
                    arg_ast.end,
                )
                log.warning(str(eval_error))
            inputs[key] = str(value)
        elif not isinstance(value, input_ast.type.to_type()):
            raise EvalError(
                f"Type of argument '{key}' do not match to with inputs declared "
                f"type. Argument has type '{type(value).__name__}', declared "
                f"input type is '{input_ast.type.value}'",
                arg_ast.start,
                arg_ast.end,
            )
    for name, inp in ast_inputs.items():
        if name not in inputs and inp.default.pattern is not None:
            val = await inp.default.eval(EMPTY_ROOT)
            # inputs doesn't support expressions,
            # non-none pattern means non-none input
            assert val is not None
            inputs[name] = val
    return inputs


async def setup_params_ctx(
    ctx: RootABC,
    params: Optional[Mapping[str, str]],
    ast_params: Optional[Mapping[str, ast.Param]],
) -> ParamsCtx:
    if params is None:
        params = {}
    new_params = {}
    if ast_params is not None:
        for k, v in ast_params.items():
            value = params.get(k)
            if value is None:
                value = await v.default.eval(ctx)
            if value is None:
                raise EvalError(
                    f"Param {k} is not initialized and has no default value",
                    v._start,
                    v._end,
                )
            new_params[k] = value
    extra = params.keys() - new_params.keys()
    if extra:
        raise ValueError(
            f"Unsupported arg(s): {','.join(sorted(extra))}",
        )
    return new_params


async def setup_strategy_ctx(
    ctx: RootABC,
    ast_defaults: Optional[ast.BatchFlowDefaults],
    ast_global_defaults: Optional[ast.BatchFlowDefaults],
) -> StrategyCtx:
    if ast_defaults is not None and ast_global_defaults is not None:
        ast_defaults = await merge_asts(ast_defaults, ast_global_defaults)
    elif ast_global_defaults:
        ast_defaults = ast_global_defaults
    if ast_defaults is None:
        return StrategyCtx()
    fail_fast = await ast_defaults.fail_fast.eval(ctx)
    if fail_fast is None:
        fail_fast = StrategyCtx.fail_fast
    max_parallel = await ast_defaults.max_parallel.eval(ctx)
    if max_parallel is None:
        max_parallel = StrategyCtx.max_parallel
    return StrategyCtx(fail_fast=fail_fast, max_parallel=max_parallel)


async def setup_matrix(
    ctx: RootABC,
    ast_matrix: Optional[ast.Matrix],
) -> Sequence[MatrixCtx]:
    if ast_matrix is None:
        return [{}]
    # Init
    products = []
    for k, lst in ast_matrix.products.items():
        values = await lst.eval(ctx)
        if values:
            lst2 = [{k: v} for v in values]
            products.append(lst2)
    matrices = []
    for row in itertools.product(*products):
        dct: Dict[str, LiteralT] = {}
        for elem in row:
            dct.update(elem)  # type: ignore[arg-type]
        matrices.append(dct)
    # Exclude
    exclude = []
    for exc_spec in ast_matrix.exclude:
        exclude.append({k: await v.eval(ctx) for k, v in exc_spec.items()})
    filtered = []
    for matrix in matrices:
        include = True
        for exc in exclude:
            match = True
            for k, v in exc.items():
                if matrix[k] != v:
                    match = False
                    break
            if match:
                include = False
                break
        if include:
            filtered.append(matrix)
    matrices = filtered
    # Include
    for inc_spec in ast_matrix.include:
        if inc_spec.keys() != ast_matrix.products.keys():
            additional = inc_spec.keys() - ast_matrix.products.keys()
            missing = ast_matrix.products.keys() - inc_spec.keys()
            raise EvalError(
                "Keys of entry in include list of matrix are not the "
                "same as matrix keys: "
                + (
                    f"additional keys: {','.join(sorted(additional))}"
                    if additional
                    else ""
                )
                + (f" , " if additional and missing else "")
                + (f"missing keys: {','.join(sorted(missing))}" if missing else ""),
                ast_matrix._start,
                ast_matrix._end,
            )
        matrices.append({k: await v.eval(ctx) for k, v in inc_spec.items()})
    for pos, dct in enumerate(matrices):
        dct["ORDINAL"] = pos
    return matrices


async def setup_cache(
    ctx: RootABC,
    base_cache: CacheConf,
    ast_cache: Optional[ast.Cache],
    default_strategy: ast.CacheStrategy,
) -> CacheConf:
    if ast_cache is None:
        return base_cache

    strategy = ast_cache.strategy
    if strategy is None:
        strategy = default_strategy
    if strategy == ast.CacheStrategy.INHERIT:
        strategy = base_cache.strategy

    life_span = await ast_cache.life_span.eval(ctx)
    if life_span is None:
        life_span = base_cache.life_span
    else:
        life_span = min(base_cache.life_span, life_span)
    return CacheConf(strategy=strategy, life_span=life_span)


def check_module_call_is_local(action_name: str, call_ast: ast.BaseModuleCall) -> None:
    if not ActionSpec.parse(action_name).is_local:
        raise EvalError(
            f"Module call to non local action '{action_name}' is forbidden",
            start=call_ast._start,
            end=call_ast._end,
        )


class SupportsAstMerge(Protocol):
    @property
    def _specified_fields(self) -> AbstractSet[str]: ...


_MergeTarget = TypeVar("_MergeTarget", bound=SupportsAstMerge)


async def merge_asts(child: _MergeTarget, parent: SupportsAstMerge) -> _MergeTarget:
    child_fields = {f.name for f in dataclasses.fields(child)}  # type: ignore
    for field in parent._specified_fields:
        if field == "mixins" or field not in child_fields:
            continue
        field_present = field in child._specified_fields
        child_value = getattr(child, field)
        parent_value = getattr(parent, field)
        merge_supported = isinstance(parent_value, BaseSequenceExpr) or isinstance(
            parent_value, BaseMappingExpr
        )
        if not field_present or (child_value is None and merge_supported):
            child = replace(
                child,
                **{field: parent_value},
                _specified_fields=child._specified_fields | {field},
            )  # type: ignore
        elif isinstance(parent_value, BaseSequenceExpr):
            assert isinstance(child_value, BaseSequenceExpr)
            child = replace(
                child, **{field: ConcatSequenceExpr(child_value, parent_value)}
            )  # type: ignore
        elif isinstance(parent_value, BaseMappingExpr):
            assert isinstance(child_value, BaseMappingExpr)
            child = replace(
                child, **{field: MergeMappingsExpr(child_value, parent_value)}
            )  # type: ignore
    return child


class MixinApplyTarget(Protocol):
    @property
    def mixins(self) -> Optional[Sequence[StrExpr]]: ...

    @property
    def _specified_fields(self) -> AbstractSet[str]: ...


_MixinApplyTarget = TypeVar("_MixinApplyTarget", bound=MixinApplyTarget)


async def apply_mixins(
    base: _MixinApplyTarget, mixins: Mapping[str, SupportsAstMerge]
) -> _MixinApplyTarget:
    if base.mixins is None:
        return base
    for mixin_expr in reversed(base.mixins):
        mixin_name = await mixin_expr.eval(EMPTY_ROOT)
        try:
            mixin = mixins[mixin_name]
        except KeyError:
            raise EvalError(
                f"Unknown mixin '{mixin_name}'",
                start=mixin_expr.start,
                end=mixin_expr.end,
            )
        base = await merge_asts(base, mixin)
    return base


async def setup_mixins(
    raw_mixins: Optional[Mapping[str, _MixinApplyTarget]]
) -> Mapping[str, _MixinApplyTarget]:
    if raw_mixins is None:
        return {}
    graph: Dict[str, Dict[str, int]] = {}
    for mixin_name, mixin in raw_mixins.items():
        mixins = mixin.mixins or []
        graph[mixin_name] = {await dep_expr.eval(EMPTY_ROOT): 1 for dep_expr in mixins}
    topo = ColoredTopoSorter(graph)
    result: Dict[str, _MixinApplyTarget] = {}
    while not topo.is_all_colored(1):
        for mixin_name in topo.get_ready():
            result[mixin_name] = await apply_mixins(raw_mixins[mixin_name], result)
            topo.mark(mixin_name, 1)
    return result


class RunningLiveFlow:
    _ast_flow: ast.LiveFlow
    _ctx: LiveContext
    _cl: ConfigLoader
    _mixins: Mapping[str, SupportsAstMerge]

    def __init__(
        self,
        ast_flow: ast.LiveFlow,
        ctx: LiveContext,
        config_loader: ConfigLoader,
        defaults: DefaultsConf,
        mixins: Mapping[str, SupportsAstMerge],
    ):
        self._ast_flow = ast_flow
        self._ctx = ctx
        self._cl = config_loader
        self._defaults = defaults
        self._mixins = mixins

    @property
    def job_ids(self) -> Iterable[str]:
        return sorted(self._ast_flow.jobs)

    @property
    def project(self) -> ProjectCtx:
        return self._ctx.project

    @property
    def flow(self) -> FlowCtx:
        return self._ctx.flow

    @property
    def tags(self) -> AbstractSet[str]:
        return self._ctx.tags

    @property
    def volumes(self) -> Mapping[str, VolumeCtx]:
        return self._ctx.volumes

    @property
    def images(self) -> Mapping[str, ImageCtx]:
        return self._ctx.images

    async def is_multi(self, job_id: str) -> bool:
        # Simple shortcut
        return (await self.get_meta(job_id)).multi

    async def _get_job_ast(
        self, job_id: str
    ) -> Union[ast.Job, ast.JobActionCall, ast.JobModuleCall]:
        try:
            base = self._ast_flow.jobs[job_id]
            if isinstance(base, ast.Job):
                base = await apply_mixins(base, self._mixins)
            return base
        except KeyError:
            raise UnknownJob(job_id)

    async def _get_action_ast(
        self, call_ast: Union[ast.JobActionCall, ast.JobModuleCall]
    ) -> ast.LiveAction:
        if isinstance(call_ast, ast.JobActionCall):
            action_name = await call_ast.action.eval(EMPTY_ROOT)
        else:
            action_name = await call_ast.module.eval(EMPTY_ROOT)
            check_module_call_is_local(action_name, call_ast)
        action_ast = await self._cl.fetch_action(action_name)
        if action_ast.kind != ast.ActionKind.LIVE:
            raise TypeError(
                f"Invalid action '{action_ast}' "
                f"type {action_ast.kind.value} for live flow"
            )
        assert isinstance(action_ast, ast.LiveAction)
        return action_ast

    async def get_meta(self, job_id: str) -> JobMeta:
        job_ast = await self._get_job_ast(job_id)

        if isinstance(job_ast, (ast.JobActionCall, ast.JobModuleCall)):
            action_ast = await self._get_action_ast(job_ast)
            multi = await action_ast.job.multi.eval(EMPTY_ROOT)
        else:
            multi = await job_ast.multi.eval(EMPTY_ROOT)

        tags = set(self.tags)
        tags.add(f"job:{_id2tag(job_id)}")
        return JobMeta(
            id=job_id,
            multi=bool(multi),
            tags=tags,
        )

    async def get_job(self, job_id: str, params: Mapping[str, str]) -> Job:
        assert not await self.is_multi(
            job_id
        ), "Use get_multi_job() for multi jobs instead of get_job()"
        job_ast = await self._get_job_ast(job_id)
        ctx = self._ctx.to_job_ctx(
            params=await setup_params_ctx(self._ctx, params, job_ast.params)
        )
        return await self._get_job(ctx, ctx.env, self._defaults, job_id)

    async def get_multi_job(
        self,
        job_id: str,
        suffix: str,
        args: Optional[Sequence[str]],
        params: Mapping[str, str],
    ) -> Job:
        assert await self.is_multi(
            job_id
        ), "Use get_job() for not multi jobs instead of get_multi_job()"

        if args is None:
            args_str = ""
        else:
            args_str = " ".join(shlex.quote(arg) for arg in args)
        job_ast = await self._get_job_ast(job_id)
        ctx = self._ctx.to_multi_job_ctx(
            multi=MultiCtx(suffix=suffix, args=args_str),
            params=await setup_params_ctx(self._ctx, params, job_ast.params),
        )
        job = await self._get_job(ctx, ctx.env, self._defaults, job_id)
        return replace(job, tags=job.tags | {f"multi:{suffix}"})

    async def _get_job(
        self,
        ctx: RootABC,
        env_ctx: EnvCtx,
        defaults: DefaultsConf,
        job_id: str,
    ) -> Job:
        job = await self._get_job_ast(job_id)
        if isinstance(job, ast.JobActionCall):
            action_ast = await self._get_action_ast(job)
            ctx = LiveActionContext(
                flow=self.flow.with_action(
                    action_path=action_ast._start.filename.parent
                ),
                inputs=await setup_inputs_ctx(ctx, job, action_ast.inputs),
                _client=self._ctx._client,
                _dry_run=self._ctx._dry_run,
            )
            env_ctx = {}
            defaults = DefaultsConf()
            job = action_ast.job
        if isinstance(job, ast.JobModuleCall):
            action_ast = await self._get_action_ast(job)
            ctx = LiveModuleContext(
                inputs=await setup_inputs_ctx(ctx, job, action_ast.inputs),
                _parent=ctx,
                _client=self._ctx._client,
                _dry_run=self._ctx._dry_run,
            )
            job = action_ast.job
        assert isinstance(job, ast.Job)

        tags = (await self.get_meta(job_id)).tags
        if job.tags is not None:
            tmp_tags = await job.tags.eval(ctx)
            assert isinstance(tmp_tags, list)
            tags |= set(tmp_tags)

        env = dict(env_ctx)
        if job.env is not None:
            tmp_env = await job.env.eval(ctx)
            assert isinstance(tmp_env, dict)
            env.update(tmp_env)

        title = await job.title.eval(ctx)
        if title is None:
            title = f"{self._ctx.flow.flow_id}.{job_id}"

        workdir = (await job.workdir.eval(ctx)) or defaults.workdir

        volumes: List[str] = list(defaults.volumes)
        if job.volumes is not None:
            tmp_volumes = await job.volumes.eval(ctx)
            assert isinstance(tmp_volumes, list)
            for volume in tmp_volumes:
                if volume:
                    volumes.append(volume)

        life_span = (await job.life_span.eval(ctx)) or defaults.life_span

        preset = (await job.preset.eval(ctx)) or defaults.preset
        schedule_timeout = (
            await job.schedule_timeout.eval(ctx)
        ) or defaults.schedule_timeout
        port_forward: List[str] = []
        if job.port_forward is not None:
            tmp_port_forward = await job.port_forward.eval(ctx)
            assert isinstance(tmp_port_forward, list)
            port_forward = tmp_port_forward

        image = await job.image.eval(ctx)
        if image is None:
            raise EvalError(
                f"Image for job {job_id} is not specified",
                start=job.image.start,
                end=job.image.end,
            )
        return Job(
            id=job_id,
            detach=bool(await job.detach.eval(ctx)),
            browse=bool(await job.browse.eval(ctx)),
            title=title,
            name=await job.name.eval(ctx),
            image=image,
            preset=preset,
            schedule_timeout=schedule_timeout,
            entrypoint=await job.entrypoint.eval(ctx),
            cmd=await job.cmd.eval(ctx),
            workdir=workdir,
            volumes=volumes,
            life_span=life_span,
            http_port=await job.http_port.eval(ctx),
            http_auth=await job.http_auth.eval(ctx),
            pass_config=await job.pass_config.eval(ctx),
            port_forward=port_forward,
            multi=await self.is_multi(job_id),
            env=env,
            tags=tags,
            restart=await job.restart.eval(ctx),
        )

    @classmethod
    async def create(
        cls,
        config_loader: ConfigLoader,
        config_name: str = "live",
        dry_run: bool = False,
    ) -> "RunningLiveFlow":
        ast_flow = await config_loader.fetch_flow(config_name)
        ast_project = await config_loader.fetch_project()

        assert isinstance(ast_flow, ast.LiveFlow)

        project_ctx = await setup_project_ctx(EMPTY_ROOT, config_loader)
        flow_ctx = await setup_flow_ctx(
            EMPTY_ROOT, ast_flow, config_name, config_loader, project_ctx
        )
        git_ctx = GitCtx(await collect_git_info())

        step_1_ctx = LiveContextStep1(
            project=project_ctx,
            flow=flow_ctx,
            git=git_ctx,
            _client=config_loader.client,
            _dry_run=dry_run,
        )

        defaults, env, tags = await setup_defaults_env_tags_ctx(
            step_1_ctx, ast_flow.defaults, ast_project.defaults
        )

        volumes = {
            **(await setup_volumes_ctx(step_1_ctx, ast_project.volumes)),
            **(await setup_volumes_ctx(step_1_ctx, ast_flow.volumes)),
        }

        images = {
            **(await setup_images_ctx(step_1_ctx, step_1_ctx, ast_project.images)),
            **(await setup_images_ctx(step_1_ctx, step_1_ctx, ast_flow.images)),
        }

        live_ctx = step_1_ctx.to_live_ctx(
            env=env,
            tags=tags,
            volumes=volumes,
            images=images,
        )

        raw_mixins: Mapping[str, MixinApplyTarget] = {
            **(ast_project.mixins or {}),
            **(ast_flow.mixins or {}),
        }
        mixins = await setup_mixins(raw_mixins)

        return cls(ast_flow, live_ctx, config_loader, defaults, mixins)


_T = TypeVar("_T", bound=BaseBatchContext, covariant=True)


class EarlyBatch:
    def __init__(
        self,
        ctx: WithFlowContext[BatchFlowCtx],
        tasks: Mapping[str, "BaseEarlyTask"],
        config_loader: ConfigLoader,
    ):
        self._flow_ctx: WithFlowContext[BatchFlowCtx] = ctx
        self._cl = config_loader
        self._tasks = tasks

    @property
    def graph(self) -> Mapping[str, Mapping[str, ast.NeedsLevel]]:
        return self._graph()

    @property
    @abstractmethod
    def mixins(self) -> Optional[Mapping[str, SupportsAstMerge]]:
        pass

    @property
    @abstractmethod
    def early_images(self) -> Mapping[str, EarlyImageCtx]:
        pass

    @abstractmethod
    def get_image_ast(self, image_id: str) -> ast.Image:
        pass

    @lru_cache()
    def _graph(self) -> Mapping[str, Mapping[str, ast.NeedsLevel]]:
        # This function is only needed for mypy
        return {key: early_task.needs for key, early_task in self._tasks.items()}

    def _get_prep(self, real_id: str) -> "BaseEarlyTask":
        try:
            return self._tasks[real_id]
        except KeyError:
            raise UnknownTask(real_id)

    async def is_task(self, real_id: str) -> bool:
        early_task = self._get_prep(real_id)
        return isinstance(early_task, EarlyTask)

    async def is_local(self, real_id: str) -> bool:
        early_task = self._get_prep(real_id)
        return isinstance(early_task, EarlyLocalCall)

    async def is_action(self, real_id: str) -> bool:
        early_task = self._get_prep(real_id)
        return isinstance(early_task, (EarlyBatchCall, EarlyModuleCall))

    async def state_from(self, real_id: str) -> Optional[str]:
        prep_task = self._get_prep(real_id)
        if isinstance(prep_task, EarlyPostTask):
            return prep_task.state_from
        return None

    def _task_context_class(self) -> Type[Context]:
        return BatchTaskContext

    def _known_inputs(self) -> AbstractSet[str]:
        return set()

    def validate_expressions(self) -> List[EvalError]:
        from .expr_validation import validate_expr

        errors: List[EvalError] = []
        for task in self._tasks.values():
            ctx_cls = self._task_context_class()
            known_needs = task.needs.keys()
            known_inputs = self._known_inputs()
            errors += validate_expr(task.enable, ctx_cls, known_needs, known_inputs)
            if isinstance(task, EarlyTask):
                _ctx_cls = ctx_cls
                if isinstance(task, EarlyStatefulCall):
                    _ctx_cls = StatefulActionContext
                    known_inputs = (task.action.inputs or {}).keys()
                ast_task = task.ast_task
                for field in fields(ast.ExecUnit):
                    field_value = getattr(ast_task, field.name)
                    if field_value is not None and isinstance(field_value, Expr):
                        errors += validate_expr(
                            field_value, _ctx_cls, known_needs, known_inputs
                        )
            if isinstance(task, (BaseEarlyCall, EarlyModuleCall)):
                args = task.call.args or {}
                for arg_expr in args.values():
                    errors += validate_expr(
                        arg_expr, ctx_cls, known_needs, known_inputs
                    )
            if isinstance(task, EarlyLocalCall):
                known_inputs = (task.action.inputs or {}).keys()
                errors += validate_expr(
                    task.action.cmd, LocalActionContext, known_inputs=known_inputs
                )
        return errors

    async def get_action_early(self, real_id: str) -> "EarlyBatchAction":
        assert await self.is_action(
            real_id
        ), f"get_action_early() cannot be used for task {real_id}"
        prep_task = cast(
            Union[EarlyBatchCall, EarlyModuleCall], self._get_prep(real_id)
        )  # Already checked

        await validate_action_call(prep_task.call, prep_task.action.inputs)

        if isinstance(prep_task, EarlyModuleCall):
            parent_ctx: Type[RootABC] = self._task_context_class()
            mixins = self.mixins
        else:
            parent_ctx = EmptyRoot
            mixins = None

        # TODO: fix typing incompatibility
        ctx = replace(
            self._flow_ctx,
            flow=self._flow_ctx.flow.with_action(  # type: ignore[arg-type]
                prep_task.action._start.filename.parent
            ),
        )

        tasks = await EarlyTaskGraphBuilder(
            ctx, self._cl, prep_task.action.tasks, mixins
        ).build()
        early_images = await setup_images_early(
            ctx, self._flow_ctx, prep_task.action.images
        )

        return EarlyBatchAction(
            ctx,
            tasks,
            early_images,
            self._cl,
            prep_task.action,
            parent_ctx,
            mixins,
        )

    async def get_local_early(self, real_id: str) -> "EarlyLocalCall":
        assert await self.is_local(
            real_id
        ), f"get_local_early() cannot used for action call {real_id}"
        prep_task = self._get_prep(real_id)
        assert isinstance(prep_task, EarlyLocalCall)  # Already checked
        return prep_task


class EarlyBatchAction(EarlyBatch):
    def __init__(
        self,
        ctx: WithFlowContext[BatchFlowCtx],
        tasks: Mapping[str, "BaseEarlyTask"],
        early_images: Mapping[str, EarlyImageCtx],
        config_loader: ConfigLoader,
        action: ast.BatchAction,
        parent_ctx_class: Type[RootABC],
        mixins: Optional[Mapping[str, SupportsAstMerge]],
    ):
        super().__init__(ctx, tasks, config_loader)
        self._action = action
        self._early_images = early_images
        self._parent_ctx_class = parent_ctx_class
        self._mixins = mixins

    @property
    def early_images(self) -> Mapping[str, EarlyImageCtx]:
        return self._early_images

    @property
    def mixins(self) -> Optional[Mapping[str, SupportsAstMerge]]:
        return self._mixins

    def get_image_ast(self, image_id: str) -> ast.Image:
        if self._action.images is None:
            raise KeyError(image_id)
        return self._action.images[image_id]

    def _task_context_class(self) -> Type[Context]:
        return BatchActionTaskContext[self._parent_ctx_class]  # type: ignore

    def _known_inputs(self) -> AbstractSet[str]:
        return (self._action.inputs or {}).keys()

    def validate_expressions(self) -> List[EvalError]:
        from .expr_validation import validate_expr

        errors = super().validate_expressions()
        known_inputs = self._known_inputs()

        if self._action.cache:
            errors += validate_expr(
                self._action.cache.life_span,
                BatchActionContext,
                known_inputs=known_inputs,
            )
        outputs = self._action.outputs

        tasks_ids = self._tasks.keys()
        if outputs and outputs.values:
            for output in outputs.values.values():
                errors += validate_expr(
                    output.value,
                    BatchActionOutputsContext,
                    known_needs=tasks_ids,
                    known_inputs=known_inputs,
                )
        return errors


class RunningBatchBase(Generic[_T], EarlyBatch, ABC):
    _tasks: Mapping[str, "BasePrepTask"]

    def __init__(
        self,
        flow_ctx: WithFlowContext[BatchFlowCtx],
        ctx: _T,
        default_tags: TagsCtx,
        tasks: Mapping[str, "BasePrepTask"],
        config_loader: ConfigLoader,
        defaults: DefaultsConf,
        bake_id: str,
        local_info: Optional[LocallyPreparedInfo],
    ):
        super().__init__(flow_ctx, tasks, config_loader)
        self._ctx = ctx
        self._default_tags = default_tags
        self._bake_id = bake_id
        self._defaults = defaults
        self._local_info = local_info

    @property
    def early_images(self) -> Mapping[str, EarlyImageCtx]:
        return self._ctx.images

    @property
    def images(self) -> Mapping[str, ImageCtx]:
        return self._ctx.images

    def _get_prep(self, real_id: str) -> "BasePrepTask":
        prep_task = super()._get_prep(real_id)
        assert isinstance(prep_task, BasePrepTask)
        return prep_task

    def _task_context(
        self, real_id: str, needs: NeedsCtx, state: StateCtx
    ) -> BaseTaskContext:
        prep_task = self._get_prep(real_id)
        needs_completed = {
            task_id
            for task_id, level in prep_task.needs.items()
            if level == ast.NeedsLevel.COMPLETED
        }
        if needs.keys() != needs_completed:
            extra = ",".join(needs.keys() - needs_completed)
            missing = ",".join(needs_completed - needs.keys())
            err = ["Error in 'needs':"]
            if extra:
                err.append(f"unexpected keys {extra}")
            if missing:
                err.append(f"missing keys {missing}")
            raise ValueError(" ".join(err))
        return self._ctx.to_matrix_ctx(
            matrix=prep_task.matrix,
            strategy=prep_task.strategy,
        ).to_task_ctx(
            needs=needs,
            state=state,
        )

    async def get_meta(
        self, real_id: str, needs: NeedsCtx, state: StateCtx
    ) -> TaskMeta:
        prep_task = self._get_prep(real_id)
        ctx = self._task_context(real_id, needs, state)
        return TaskMeta(
            enable=await prep_task.enable.eval(ctx),
            strategy=prep_task.strategy,
            cache=prep_task.cache,
        )

    async def get_task(
        self, prefix: FullID, real_id: str, needs: NeedsCtx, state: StateCtx
    ) -> Task:
        assert await self.is_task(
            real_id
        ), f"get_task() cannot be used for tasks action call with id {real_id}"
        prep_task = self._get_prep(real_id)
        assert isinstance(prep_task, (PrepTask, PrepStatefulCall))  # Already checked

        task_ctx = self._task_context(real_id, needs, state)
        ctx: RootABC = task_ctx
        defaults = self._defaults

        if isinstance(prep_task, PrepStatefulCall):
            ctx = StatefulActionContext(
                inputs=await setup_inputs_ctx(
                    ctx, prep_task.call, prep_task.action.inputs
                ),
                _client=self._ctx._client,
                _dry_run=self._ctx._dry_run,
            )
            defaults = DefaultsConf()  # TODO: Is it correct?

        full_id = prefix + (real_id,)

        try:
            env_ctx = ctx.lookup("env")
            assert isinstance(env_ctx, dict)
            env: Dict[str, str] = dict(env_ctx)
        except NotAvailable:
            env = {}

        if prep_task.ast_task.env is not None:
            tmp_env = await prep_task.ast_task.env.eval(ctx)
            assert isinstance(tmp_env, dict)
            env.update(tmp_env)

        title = await prep_task.ast_task.title.eval(ctx)

        tags = set()
        if prep_task.ast_task.tags is not None:
            tmp_tags = await prep_task.ast_task.tags.eval(ctx)
            assert isinstance(tmp_tags, list)
            tags |= set(tmp_tags)

        tags |= {"task:" + _id2tag(".".join(full_id))}
        tags |= set(self._default_tags)

        workdir = (await prep_task.ast_task.workdir.eval(ctx)) or defaults.workdir

        volumes: List[str] = list(defaults.volumes)
        if prep_task.ast_task.volumes is not None:
            tmp_volumes = await prep_task.ast_task.volumes.eval(ctx)
            assert isinstance(tmp_volumes, list)
            for val in tmp_volumes:
                if val:
                    volumes.append(val)

        life_span = (await prep_task.ast_task.life_span.eval(ctx)) or defaults.life_span

        preset = (await prep_task.ast_task.preset.eval(ctx)) or defaults.preset
        schedule_timeout = (
            await prep_task.ast_task.schedule_timeout.eval(ctx)
        ) or defaults.schedule_timeout
        # Enable should be calculated using outer ctx for stateful calls
        enable = (await self.get_meta(real_id, needs, state)).enable

        image = await prep_task.ast_task.image.eval(ctx)
        if image is None:
            # Should be validated out earlier, but just in case
            raise EvalError(
                f"Image for task {prep_task.real_id} is not specified",
                start=prep_task.ast_task.image.start,
                end=prep_task.ast_task.image.end,
            )
        task = Task(
            id=prep_task.id,
            title=title,
            name=(await prep_task.ast_task.name.eval(ctx)),
            image=image,
            preset=preset,
            schedule_timeout=schedule_timeout,
            entrypoint=await prep_task.ast_task.entrypoint.eval(ctx),
            cmd=await prep_task.ast_task.cmd.eval(ctx),
            workdir=workdir,
            volumes=volumes,
            life_span=life_span,
            http_port=await prep_task.ast_task.http_port.eval(ctx),
            http_auth=await prep_task.ast_task.http_auth.eval(ctx),
            pass_config=await prep_task.ast_task.pass_config.eval(ctx),
            enable=enable,
            cache=prep_task.cache,
            strategy=prep_task.strategy,
            tags=tags,
            env=env,
            caching_key="",
            restart=await prep_task.ast_task.restart.eval(ctx),
        )
        return replace(
            task,
            tags=task.tags | {f"bake_id:{self._bake_id}"},
            caching_key=_hash(dict(task=task, needs=needs, state=state)),
        )

    async def get_action(
        self, real_id: str, needs: NeedsCtx
    ) -> "RunningBatchActionFlow":
        assert await self.is_action(
            real_id
        ), f"get_task() cannot used for action call {real_id}"
        prep_task = cast(
            Union[PrepBatchCall, PrepModuleCall], self._get_prep(real_id)
        )  # Already checked

        ctx = self._task_context(real_id, needs, {})

        if isinstance(prep_task, PrepModuleCall):
            parent_ctx: RootABC = ctx
            defaults = self._defaults
            mixins = self.mixins
        else:
            parent_ctx = EMPTY_ROOT
            defaults = DefaultsConf()
            mixins = None

        return await RunningBatchActionFlow.create(
            flow_ctx=self._flow_ctx,
            parent_ctx=parent_ctx,
            ast_action=prep_task.action,
            base_cache=prep_task.cache,
            base_strategy=prep_task.strategy,
            inputs=await setup_inputs_ctx(ctx, prep_task.call, prep_task.action.inputs),
            default_tags=self._default_tags,
            bake_id=self._bake_id,
            local_info=(
                self._local_info.children_info.get(real_id)
                if self._local_info
                else None
            ),
            config_loader=self._cl,
            defaults=defaults,
            mixins=mixins,
        )

    async def get_local(self, real_id: str, needs: NeedsCtx) -> LocalTask:
        assert await self.is_local(
            real_id
        ), f"get_task() cannot used for action call {real_id}"
        prep_task = self._get_prep(real_id)
        assert isinstance(prep_task, PrepLocalCall)  # Already checked

        ctx = self._task_context(real_id, needs, {})

        action_ctx = LocalActionContext(
            inputs=await setup_inputs_ctx(ctx, prep_task.call, prep_task.action.inputs),
            _client=self._ctx._client,
            _dry_run=self._ctx._dry_run,
        )

        return LocalTask(
            id=prep_task.id,
            cmd=await prep_task.action.cmd.eval(action_ctx),
        )


class RunningBatchFlow(RunningBatchBase[BatchContext]):
    def __init__(
        self,
        ctx: BatchContext,
        tasks: Mapping[str, "BasePrepTask"],
        config_loader: ConfigLoader,
        defaults: DefaultsConf,
        bake_id: str,
        local_info: Optional[LocallyPreparedInfo],
        ast_flow: ast.BatchFlow,
        ast_project: ast.Project,
        mixins: Optional[Mapping[str, SupportsAstMerge]],
    ):
        super().__init__(
            ctx,
            ctx,
            ctx.tags,
            tasks,
            config_loader,
            defaults,
            bake_id,
            local_info,
        )
        self._ast_flow = ast_flow
        self._ast_project = ast_project
        self._mixins = mixins

    def get_image_ast(self, image_id: str) -> ast.Image:
        try:
            if self._ast_flow.images is None:
                raise KeyError(image_id)
            return self._ast_flow.images[image_id]
        except KeyError:
            if self._ast_project.images is not None:
                return self._ast_project.images[image_id]
            raise

    @property
    def mixins(self) -> Optional[Mapping[str, SupportsAstMerge]]:
        return self._mixins

    @property
    def params(self) -> Mapping[str, str]:
        return self._ctx.params

    @property
    def project_id(self) -> str:
        return self._ctx.flow.project_id

    @property
    def project_name(self) -> str:
        return self._ctx.project.project_name

    @property
    def volumes(self) -> Mapping[str, VolumeCtx]:
        return self._ctx.volumes

    @property
    def life_span(self) -> Optional[timedelta]:
        if self._ctx.flow.life_span:
            return timedelta(seconds=self._ctx.flow.life_span)
        return None

    @property
    def workspace(self) -> LocalPath:
        return self._ctx.flow.workspace

    @classmethod
    async def create(
        cls,
        config_loader: ConfigLoader,
        batch: str,
        bake_id: str,
        params: Optional[Mapping[str, str]] = None,
        local_info: Optional[LocallyPreparedInfo] = None,
        dry_run: bool = False,
    ) -> "RunningBatchFlow":
        ast_flow = await config_loader.fetch_flow(batch)
        ast_project = await config_loader.fetch_project()

        assert isinstance(ast_flow, ast.BatchFlow)

        project_ctx = await setup_project_ctx(EMPTY_ROOT, config_loader)
        flow_ctx = await setup_batch_flow_ctx(
            EMPTY_ROOT, ast_flow, batch, config_loader, project_ctx
        )

        params_ctx = await setup_params_ctx(EMPTY_ROOT, params, ast_flow.params)
        step_1_ctx = BatchContextStep1(
            project=project_ctx,
            flow=flow_ctx,
            params=params_ctx,
            git=GitCtx(local_info.git_info if local_info else None),
            _client=config_loader.client,
            _dry_run=dry_run,
        )
        if local_info is None:
            early_images: Mapping[str, EarlyImageCtx] = {
                **(
                    await setup_images_early(step_1_ctx, step_1_ctx, ast_project.images)
                ),
                **(await setup_images_early(step_1_ctx, step_1_ctx, ast_flow.images)),
            }
        else:
            early_images = local_info.early_images

        defaults, env, tags = await setup_defaults_env_tags_ctx(
            step_1_ctx, ast_flow.defaults, ast_project.defaults
        )

        volumes = {
            **(await setup_volumes_ctx(step_1_ctx, ast_project.volumes)),
            **(await setup_volumes_ctx(step_1_ctx, ast_flow.volumes)),
        }

        images = {
            **(
                await setup_images_ctx(
                    step_1_ctx, step_1_ctx, ast_project.images, early_images
                )
            ),
            **(
                await setup_images_ctx(
                    step_1_ctx, step_1_ctx, ast_flow.images, early_images
                )
            ),
        }

        step_2_ctx = step_1_ctx.to_step_2(
            env=env,
            tags=tags,
            volumes=volumes,
            images=images,
        )

        if ast_project.defaults:
            base_cache = await setup_cache(
                step_2_ctx,
                CacheConf(),
                ast_project.defaults.cache,
                ast.CacheStrategy.INHERIT,
            )
        else:
            base_cache = CacheConf()

        if ast_flow.defaults:
            ast_cache = ast_flow.defaults.cache
        else:
            ast_cache = None
        cache_conf = await setup_cache(
            step_2_ctx, base_cache, ast_cache, ast.CacheStrategy.INHERIT
        )

        batch_ctx = step_2_ctx.to_batch_ctx(
            strategy=await setup_strategy_ctx(
                step_2_ctx, ast_flow.defaults, ast_project.defaults
            ),
        )

        raw_mixins: Mapping[str, MixinApplyTarget] = {
            **(ast_project.mixins or {}),
            **(ast_flow.mixins or {}),
        }
        mixins = await setup_mixins(raw_mixins)
        tasks = await TaskGraphBuilder(
            batch_ctx, config_loader, cache_conf, ast_flow.tasks, mixins
        ).build()

        return RunningBatchFlow(
            batch_ctx,
            tasks,
            config_loader,
            defaults,
            bake_id,
            local_info,
            ast_flow,
            ast_project,
            mixins,
        )


class RunningBatchActionFlow(RunningBatchBase[BatchActionContext[RootABC]]):
    def __init__(
        self,
        flow_ctx: WithFlowContext[BatchFlowCtx],
        ctx: BatchActionContext[RootABC],
        default_tags: TagsCtx,
        tasks: Mapping[str, "BasePrepTask"],
        config_loader: ConfigLoader,
        defaults: DefaultsConf,
        action: ast.BatchAction,
        bake_id: str,
        local_info: Optional[LocallyPreparedInfo],
        mixins: Optional[Mapping[str, SupportsAstMerge]],
    ):
        super().__init__(
            flow_ctx,
            ctx,
            default_tags,
            tasks,
            config_loader,
            defaults,
            bake_id,
            local_info,
        )
        self._action = action
        self._mixins = mixins

    def get_image_ast(self, image_id: str) -> ast.Image:
        if self._action.images is None:
            raise KeyError(image_id)
        return self._action.images[image_id]

    @property
    def mixins(self) -> Optional[Mapping[str, SupportsAstMerge]]:
        return self._mixins

    async def calc_outputs(self, task_results: NeedsCtx) -> DepCtx:
        if any(i.result == TaskStatus.FAILED for i in task_results.values()):
            return DepCtx(TaskStatus.FAILED, {})
        elif any(i.result == TaskStatus.CANCELLED for i in task_results.values()):
            return DepCtx(TaskStatus.CANCELLED, {})
        else:
            ctx = self._ctx.to_outputs_ctx(task_results)
            ret = {}
            if self._action.outputs and self._action.outputs.values is not None:
                for name, descr in self._action.outputs.values.items():
                    val = await descr.value.eval(ctx)
                    assert val is not None
                    ret[name] = val
            return DepCtx(TaskStatus.SUCCEEDED, ret)

    @classmethod
    async def create(
        cls,
        flow_ctx: WithFlowContext[BatchFlowCtx],
        parent_ctx: RootABC,
        ast_action: ast.BatchAction,
        base_cache: CacheConf,
        base_strategy: StrategyCtx,
        inputs: InputsCtx,
        default_tags: TagsCtx,
        config_loader: ConfigLoader,
        bake_id: str,
        local_info: Optional[LocallyPreparedInfo],
        defaults: DefaultsConf = DefaultsConf(),
        mixins: Optional[Mapping[str, SupportsAstMerge]] = None,
    ) -> "RunningBatchActionFlow":
        step_1_ctx = BatchActionContextStep1(
            flow=flow_ctx.flow.with_action(
                action_path=ast_action._start.filename.parent
            ),
            git=GitCtx(local_info.git_info if local_info else None),
            inputs=inputs,
            strategy=base_strategy,
            _client=config_loader.client,
            _parent=parent_ctx,
            _dry_run=parent_ctx.dry_run,
        )

        if local_info is None:
            early_images = await setup_images_early(
                step_1_ctx, flow_ctx, ast_action.images
            )
        else:
            early_images = local_info.early_images

        images = await setup_images_ctx(
            step_1_ctx, flow_ctx, ast_action.images, early_images
        )

        action_context = step_1_ctx.to_action_ctx(images=images)

        cache = await setup_cache(
            action_context, base_cache, ast_action.cache, ast.CacheStrategy.INHERIT
        )

        tasks = await TaskGraphBuilder(
            action_context, config_loader, cache, ast_action.tasks, mixins
        ).build()

        return RunningBatchActionFlow(
            flow_ctx,
            action_context,
            default_tags,
            tasks,
            config_loader,
            defaults,
            ast_action,
            bake_id,
            local_info,
            mixins,
        )


# Task graph builder


@dataclass(frozen=True)
class BaseEarlyTask:
    id: Optional[str]
    real_id: str
    needs: Mapping[str, ast.NeedsLevel]  # Keys are batch.id

    matrix: MatrixCtx
    enable: EnableExpr

    def to_task(self, ast_task: ast.ExecUnit) -> "EarlyTask":
        return EarlyTask(
            id=self.id,
            real_id=self.real_id,
            needs=self.needs,
            matrix=self.matrix,
            enable=self.enable,
            ast_task=ast_task,
        )

    def to_batch_call(
        self,
        action_name: str,
        action: ast.BatchAction,
        call: ast.TaskActionCall,
    ) -> "EarlyBatchCall":
        return EarlyBatchCall(
            id=self.id,
            real_id=self.real_id,
            needs=self.needs,
            matrix=self.matrix,
            enable=self.enable,
            action_name=action_name,
            action=action,
            call=call,
        )

    def to_module_call(
        self,
        action_name: str,
        action: ast.BatchAction,
        call: ast.TaskModuleCall,
    ) -> "EarlyModuleCall":
        return EarlyModuleCall(
            id=self.id,
            real_id=self.real_id,
            needs=self.needs,
            matrix=self.matrix,
            enable=self.enable,
            action_name=action_name,
            action=action,
            call=call,
        )

    def to_local_call(
        self,
        action_name: str,
        action: ast.LocalAction,
        call: ast.TaskActionCall,
    ) -> "EarlyLocalCall":
        return EarlyLocalCall(
            id=self.id,
            real_id=self.real_id,
            needs=self.needs,
            matrix=self.matrix,
            enable=self.enable,
            action_name=action_name,
            action=action,
            call=call,
        )

    def to_stateful_call(
        self,
        action_name: str,
        action: ast.StatefulAction,
        call: ast.TaskActionCall,
    ) -> "EarlyStatefulCall":
        return EarlyStatefulCall(
            id=self.id,
            real_id=self.real_id,
            needs=self.needs,
            matrix=self.matrix,
            ast_task=action.main,
            enable=self.enable,
            action_name=action_name,
            action=action,
            call=call,
        )

    def to_post_task(self, ast_task: ast.ExecUnit, state_from: str) -> "EarlyPostTask":
        return EarlyPostTask(
            id=self.id,
            real_id=self.real_id,
            needs=self.needs,
            matrix=self.matrix,
            enable=self.enable,
            ast_task=ast_task,
            state_from=state_from,
        )

    def to_prep_base(self, strategy: StrategyCtx, cache: CacheConf) -> "BasePrepTask":
        return BasePrepTask(
            id=self.id,
            real_id=self.real_id,
            needs=self.needs,
            matrix=self.matrix,
            enable=self.enable,
            strategy=strategy,
            cache=cache,
        )


@dataclass(frozen=True)
class EarlyTask(BaseEarlyTask):
    ast_task: ast.ExecUnit


@dataclass(frozen=True)
class BaseEarlyCall(BaseEarlyTask):
    call: ast.TaskActionCall
    action_name: str


@dataclass(frozen=True)
class EarlyBatchCall(BaseEarlyCall):
    action: ast.BatchAction


@dataclass(frozen=True)
class EarlyLocalCall(BaseEarlyCall):
    action: ast.LocalAction


@dataclass(frozen=True)
class EarlyStatefulCall(EarlyTask, BaseEarlyCall):
    action: ast.StatefulAction


@dataclass(frozen=True)
class EarlyPostTask(EarlyTask):
    state_from: str


@dataclass(frozen=True)
class EarlyModuleCall(BaseEarlyTask):
    call: ast.TaskModuleCall
    action_name: str
    action: ast.BatchAction


@dataclass(frozen=True)
class BasePrepTask(BaseEarlyTask):
    strategy: StrategyCtx
    cache: CacheConf

    def to_task(self, ast_task: ast.ExecUnit) -> "PrepTask":
        return PrepTask(
            id=self.id,
            real_id=self.real_id,
            needs=self.needs,
            matrix=self.matrix,
            strategy=self.strategy,
            cache=self.cache,
            enable=self.enable,
            ast_task=ast_task,
        )

    def to_batch_call(
        self,
        action_name: str,
        action: ast.BatchAction,
        call: ast.TaskActionCall,
    ) -> "PrepBatchCall":
        return PrepBatchCall(
            id=self.id,
            real_id=self.real_id,
            needs=self.needs,
            matrix=self.matrix,
            strategy=self.strategy,
            cache=self.cache,
            enable=self.enable,
            action_name=action_name,
            action=action,
            call=call,
        )

    def to_module_call(
        self,
        action_name: str,
        action: ast.BatchAction,
        call: ast.TaskModuleCall,
    ) -> "PrepModuleCall":
        return PrepModuleCall(
            id=self.id,
            real_id=self.real_id,
            needs=self.needs,
            matrix=self.matrix,
            strategy=self.strategy,
            cache=self.cache,
            enable=self.enable,
            action_name=action_name,
            action=action,
            call=call,
        )

    def to_local_call(
        self,
        action_name: str,
        action: ast.LocalAction,
        call: ast.TaskActionCall,
    ) -> "PrepLocalCall":
        return PrepLocalCall(
            id=self.id,
            real_id=self.real_id,
            needs=self.needs,
            matrix=self.matrix,
            strategy=self.strategy,
            cache=CacheConf(strategy=ast.CacheStrategy.NONE),
            enable=self.enable,
            action_name=action_name,
            action=action,
            call=call,
        )

    def to_stateful_call(
        self,
        action_name: str,
        action: ast.StatefulAction,
        call: ast.TaskActionCall,
    ) -> "PrepStatefulCall":
        return PrepStatefulCall(
            id=self.id,
            real_id=self.real_id,
            needs=self.needs,
            matrix=self.matrix,
            strategy=self.strategy,
            cache=CacheConf(strategy=ast.CacheStrategy.NONE),
            enable=self.enable,
            action_name=action_name,
            ast_task=action.main,
            action=action,
            call=call,
        )

    def to_post_task(self, ast_task: ast.ExecUnit, state_from: str) -> "PrepPostTask":
        return PrepPostTask(
            id=self.id,
            real_id=self.real_id,
            needs=self.needs,
            matrix=self.matrix,
            strategy=self.strategy,
            cache=CacheConf(strategy=ast.CacheStrategy.NONE),
            enable=self.enable,
            ast_task=ast_task,
            state_from=state_from,
        )


@dataclass(frozen=True)
class PrepTask(EarlyTask, BasePrepTask):
    pass


@dataclass(frozen=True)
class PrepBatchCall(EarlyBatchCall, BasePrepTask):
    pass


@dataclass(frozen=True)
class PrepLocalCall(EarlyLocalCall, BasePrepTask):
    pass


@dataclass(frozen=True)
class PrepStatefulCall(EarlyStatefulCall, PrepTask):
    pass


@dataclass(frozen=True)
class PrepPostTask(EarlyPostTask, PrepTask):
    pass


@dataclass(frozen=True)
class PrepModuleCall(EarlyModuleCall, BasePrepTask):
    pass


class EarlyTaskGraphBuilder:
    MATRIX_SIZE_LIMIT = 256

    def __init__(
        self,
        ctx: RootABC,
        config_loader: ConfigLoader,
        ast_tasks: Sequence[Union[ast.Task, ast.TaskActionCall, ast.TaskModuleCall]],
        mixins: Optional[Mapping[str, SupportsAstMerge]],
    ):
        self._ctx = ctx
        self._cl = config_loader
        self._ast_tasks = ast_tasks
        self._mixins = mixins or {}

    async def _extend_base(
        self,
        base: BaseEarlyTask,
        ast_task: Union[ast.Task, ast.TaskActionCall, ast.TaskModuleCall],
    ) -> BaseEarlyTask:
        return base

    async def build(self) -> Mapping[str, BaseEarlyTask]:
        post_tasks: List[List[EarlyPostTask]] = []
        prep_tasks: Dict[str, BaseEarlyTask] = {}
        last_needs: Set[str] = set()

        # Only used for sanity checks
        real_id_to_need_to_expr: Dict[str, Mapping[str, IdExpr]] = {}

        for num, ast_task in enumerate(self._ast_tasks, 1):
            assert isinstance(
                ast_task, (ast.Task, ast.TaskActionCall, ast.TaskModuleCall)
            )

            matrix_ast = ast_task.strategy.matrix if ast_task.strategy else None
            matrices = await setup_matrix(self._ctx, matrix_ast)

            if len(matrices) > self.MATRIX_SIZE_LIMIT:
                assert matrix_ast
                raise EvalError(
                    f"The matrix size for task #{num} exceeds the limit of 256",
                    matrix_ast._start,
                    matrix_ast._end,
                )

            real_ids = set()
            post_tasks_group = []
            for matrix in matrices:
                # make prep patch(es)
                matrix_ctx = MatrixOnlyContext(
                    matrix=matrix,
                    _client=self._cl.client,
                    _dry_run=False,
                )

                task_id, real_id = await self._setup_ids(matrix_ctx, num, ast_task)
                needs, need_to_expr = await self._setup_needs(
                    matrix_ctx, last_needs, ast_task
                )
                real_id_to_need_to_expr[real_id] = need_to_expr

                base = BaseEarlyTask(
                    id=task_id,
                    real_id=real_id,
                    needs=needs,
                    matrix=matrix,
                    enable=ast_task.enable,
                )
                base = await self._extend_base(base, ast_task)

                if isinstance(ast_task, ast.Task):
                    ast_task = await apply_mixins(ast_task, self._mixins)
                    prep_tasks[real_id] = base.to_task(ast_task)
                elif isinstance(ast_task, ast.TaskModuleCall):
                    action_name = await ast_task.module.eval(EMPTY_ROOT)
                    check_module_call_is_local(action_name, ast_task)
                    action = await self._cl.fetch_action(action_name)
                    if isinstance(action, ast.BatchAction):
                        prep_tasks[real_id] = base.to_module_call(
                            action_name, action, ast_task
                        )
                    else:
                        raise ValueError(
                            f"Module call to {action_name} with "
                            f"kind {action.kind.value} "
                            "is not supported."
                        )
                else:
                    assert isinstance(ast_task, ast.TaskActionCall)
                    action_name = await ast_task.action.eval(EMPTY_ROOT)
                    action = await self._cl.fetch_action(action_name)
                    if ast_task.cache and not isinstance(action, ast.BatchAction):
                        raise EvalError(
                            f"Specifying cache in action call to the action "
                            f"{action_name} of kind {action.kind.value} is "
                            f"not supported.",
                            ast_task._start,
                            ast_task._end,
                        )
                    if isinstance(action, ast.BatchAction):
                        prep_tasks[real_id] = base.to_batch_call(
                            action_name, action, ast_task
                        )
                    elif isinstance(action, ast.LocalAction):
                        prep_tasks[real_id] = base.to_local_call(
                            action_name, action, ast_task
                        )
                    elif isinstance(action, ast.StatefulAction):
                        if action.post:
                            post_tasks_group.append(
                                replace(
                                    base,
                                    id=None,
                                    real_id=f"post-{base.real_id}",
                                    needs={real_id: ast.NeedsLevel.COMPLETED},
                                    enable=action.post_if,
                                ).to_post_task(action.post, real_id),
                            )
                        prep_tasks[real_id] = base.to_stateful_call(
                            action_name, action, ast_task
                        )

                    else:
                        raise ValueError(
                            f"Action {action_name} has kind {action.kind.value}, "
                            "that is not supported in batch mode."
                        )
                real_ids.add(real_id)

            if post_tasks_group:
                post_tasks.append(post_tasks_group)

            last_needs = real_ids

        for post_tasks_group in reversed(post_tasks):
            real_ids = set()
            for task in post_tasks_group:
                needs = {need: ast.NeedsLevel.COMPLETED for need in last_needs}
                needs = {**needs, **task.needs}
                task = replace(task, needs=needs)
                prep_tasks[task.real_id] = task
                real_ids.add(task.real_id)
            last_needs = real_ids

        # Check needs sanity
        for prep_task in prep_tasks.values():
            for need_id in prep_task.needs.keys():
                if need_id not in prep_tasks:
                    id_expr = real_id_to_need_to_expr[prep_task.real_id][need_id]
                    raise EvalError(
                        f"Task {prep_task.real_id} needs unknown task {need_id}",
                        id_expr.start,
                        id_expr.end,
                    )
        # Check that all tasks have non-null image
        for prep_task in prep_tasks.values():
            if isinstance(prep_task, EarlyTask):
                image_expr = prep_task.ast_task.image
                if image_expr.pattern is None:
                    raise EvalError(
                        f"Image for task {prep_task.real_id} is not specified",
                        image_expr.start,
                        image_expr.end,
                    )

        return prep_tasks

    async def _setup_ids(
        self, ctx: MatrixOnlyContext, num: int, ast_task: ast.TaskBase
    ) -> Tuple[Optional[str], str]:
        task_id = await ast_task.id.eval(ctx)
        if task_id is None:
            # Dash is not allowed in identifier, so the generated read id
            # never clamps with user-provided one.
            # Filter system properties
            keys = [key for key in sorted(ctx.matrix) if key == key.lower()]
            suffix = [str(ctx.matrix[key]) for key in keys]
            real_id = "-".join(["task", str(num), *suffix])
        else:
            real_id = task_id
        return task_id, real_id

    async def _setup_needs(
        self, ctx: RootABC, default_needs: AbstractSet[str], ast_task: ast.TaskBase
    ) -> Tuple[Mapping[str, ast.NeedsLevel], Mapping[str, IdExpr]]:
        if ast_task.needs is not None:
            needs, to_expr_map = {}, {}
            for need, level in ast_task.needs.items():
                need_id = await need.eval(ctx)
                needs[need_id] = level
                to_expr_map[need_id] = need
            return needs, to_expr_map
        return {need: ast.NeedsLevel.COMPLETED for need in default_needs}, {}


class TaskGraphBuilder(EarlyTaskGraphBuilder):
    MATRIX_SIZE_LIMIT = 256
    _ctx: BaseBatchContext

    def __init__(
        self,
        ctx: BaseBatchContext,
        config_loader: ConfigLoader,
        default_cache: CacheConf,
        ast_tasks: Sequence[Union[ast.Task, ast.TaskActionCall, ast.TaskModuleCall]],
        mixins: Optional[Mapping[str, SupportsAstMerge]],
    ):
        super().__init__(ctx, config_loader, ast_tasks, mixins)
        self._ctx = ctx
        self._default_cache = default_cache

    async def _extend_base(
        self,
        base: BaseEarlyTask,
        ast_task: Union[ast.Task, ast.TaskActionCall, ast.TaskModuleCall],
    ) -> BasePrepTask:
        strategy = await self._setup_strategy(ast_task.strategy)

        matrix_ctx = self._ctx.to_matrix_ctx(matrix=base.matrix, strategy=strategy)
        cache = await setup_cache(
            matrix_ctx,
            self._default_cache,
            ast_task.cache,
            ast.CacheStrategy.INHERIT,
        )

        return base.to_prep_base(strategy, cache)

    async def build(self) -> Mapping[str, BasePrepTask]:
        # Super method already returns proper type (thanks to _extend_base),
        # but it is hard to properly annotate, so we have to do runtime check here
        ret = {}
        tasks = await super().build()
        for key, value in tasks.items():
            assert isinstance(value, BasePrepTask)
            ret[key] = value
        return ret

    async def _setup_strategy(
        self, ast_strategy: Optional[ast.Strategy]
    ) -> StrategyCtx:
        if ast_strategy is None:
            return self._ctx.strategy

        fail_fast = await ast_strategy.fail_fast.eval(self._ctx)
        if fail_fast is None:
            fail_fast = self._ctx.strategy.fail_fast
        max_parallel = await ast_strategy.max_parallel.eval(self._ctx)
        if max_parallel is None:
            max_parallel = self._ctx.strategy.max_parallel

        return StrategyCtx(fail_fast=fail_fast, max_parallel=max_parallel)


# Utils


def _id2tag(id: str) -> str:
    return id.replace("_", "-").lower()


def _hash(val: Any) -> str:
    hasher = hashlib.new("sha256")
    data = json.dumps(val, sort_keys=True, default=_ctx_default)
    hasher.update(data.encode("utf-8"))
    return hasher.hexdigest()


def _ctx_default(val: Any) -> Any:
    if not isinstance(val, type) and dataclasses.is_dataclass(val):
        if hasattr(val, "_client"):
            val = dataclasses.replace(val, _client=None)
        if hasattr(val, "_parent") and hasattr(val._parent, "_client"):
            parent = dataclasses.replace(val._parent, _client=None)
            val = dataclasses.replace(val, _parent=parent)
        ret = dataclasses.asdict(val)
        ret.pop("_client", None)
        return ret
    elif isinstance(val, enum.Enum):
        return val.value
    elif isinstance(val, RemotePath):
        return str(val)
    elif isinstance(val, LocalPath):
        return str(val)
    elif isinstance(val, collections.abc.Set):
        return sorted(val)
    elif isinstance(val, AlwaysT):
        return str(val)
    elif isinstance(val, URL):
        return str(val)
    elif isinstance(val, EmptyRoot):
        return {}
    else:
        raise TypeError(f"Cannot dump {val!r}")
