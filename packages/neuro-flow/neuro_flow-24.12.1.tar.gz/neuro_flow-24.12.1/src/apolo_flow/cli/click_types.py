import abc
import apolo_sdk
import click
from apolo_cli.asyncio_utils import Runner
from apolo_sdk import ResourceNotFound
from click.shell_completion import CompletionItem
from contextlib import AsyncExitStack
from typing import Generic, List, Optional, TypeVar, cast

from apolo_flow.batch_runner import BatchRunner
from apolo_flow.cli.root import Root
from apolo_flow.cli.utils import resolve_bake
from apolo_flow.live_runner import LiveRunner
from apolo_flow.storage.api import ApiStorage
from apolo_flow.storage.base import Storage


_T = TypeVar("_T")


class AsyncType(click.ParamType, Generic[_T], abc.ABC):
    def convert(
        self,
        value: str,
        param: Optional[click.Parameter],
        ctx: Optional[click.Context],
    ) -> _T:
        assert ctx is not None
        root = cast(Root, ctx.obj)
        with Runner() as runner:
            return runner.run(self.async_convert(root, value, param, ctx))

    @abc.abstractmethod
    async def async_convert(
        self,
        root: Root,
        value: str,
        param: Optional[click.Parameter],
        ctx: Optional[click.Context],
    ) -> _T:
        pass

    def shell_complete(
        self, ctx: click.Context, param: click.Parameter, incomplete: str
    ) -> List[CompletionItem]:
        root = cast(Root, ctx.obj)
        with Runner() as runner:
            return runner.run(self.async_shell_complete(root, ctx, param, incomplete))

    @abc.abstractmethod
    async def async_shell_complete(
        self, root: Root, ctx: click.Context, param: click.Parameter, incomplete: str
    ) -> List[CompletionItem]:
        pass


class LiveJobType(AsyncType[str]):
    name = "job"

    def __init__(self, allow_all: bool = False):
        self._allow_all = allow_all

    async def async_convert(
        self,
        root: Root,
        value: str,
        param: Optional[click.Parameter],
        ctx: Optional[click.Context],
    ) -> str:
        return value

    async def async_shell_complete(
        self, root: Root, ctx: click.Context, param: click.Parameter, incomplete: str
    ) -> List[CompletionItem]:
        async with AsyncExitStack() as stack:
            client = await stack.enter_async_context(apolo_sdk.get())
            storage: Storage = await stack.enter_async_context(ApiStorage(client))
            runner = await stack.enter_async_context(
                LiveRunner(root.config_dir, root.console, client, storage, root)
            )
            variants = list(runner.flow.job_ids)
            if self._allow_all:
                variants += ["ALL"]
        return [
            CompletionItem(job_id)
            for job_id in variants
            if job_id.startswith(incomplete)
        ]


LIVE_JOB = LiveJobType(allow_all=False)
LIVE_JOB_OR_ALL = LiveJobType(allow_all=True)


class LiveJobSuffixType(AsyncType[str]):
    name = "suffix"

    def __init__(self, *, job_id_param_name: str = "job_id"):
        self._job_id_param_name = job_id_param_name

    async def async_convert(
        self,
        root: Root,
        value: str,
        param: Optional[click.Parameter],
        ctx: Optional[click.Context],
    ) -> str:
        return value

    async def async_shell_complete(
        self, root: Root, ctx: click.Context, param: click.Parameter, incomplete: str
    ) -> List[CompletionItem]:
        job_id = ctx.params[self._job_id_param_name]
        async with AsyncExitStack() as stack:
            client = await stack.enter_async_context(apolo_sdk.get())
            storage: Storage = await stack.enter_async_context(ApiStorage(client))
            runner = await stack.enter_async_context(
                LiveRunner(root.config_dir, root.console, client, storage, root)
            )
            variants = await runner.list_suffixes(job_id)
        return [
            CompletionItem(suffix)
            for suffix in variants
            if suffix.startswith(incomplete)
        ]


class LiveImageType(AsyncType[str]):
    name = "image"

    def __init__(self, allow_all: bool = False):
        self._allow_all = allow_all

    async def async_convert(
        self,
        root: Root,
        value: str,
        param: Optional[click.Parameter],
        ctx: Optional[click.Context],
    ) -> str:
        return value

    async def async_shell_complete(
        self, root: Root, ctx: click.Context, param: click.Parameter, incomplete: str
    ) -> List[CompletionItem]:
        async with AsyncExitStack() as stack:
            client = await stack.enter_async_context(apolo_sdk.get())
            storage: Storage = await stack.enter_async_context(ApiStorage(client))
            runner = await stack.enter_async_context(
                LiveRunner(root.config_dir, root.console, client, storage, root)
            )
            variants = [
                image
                for image, image_ctx in runner.flow.images.items()
                if image_ctx.context is not None
            ]
            if self._allow_all:
                variants += ["ALL"]
        return [
            CompletionItem(image) for image in variants if image.startswith(incomplete)
        ]


LIVE_IMAGE_OR_ALL = LiveImageType(allow_all=True)


class LiveVolumeType(AsyncType[str]):
    name = "volume"

    def __init__(self, allow_all: bool = False):
        self._allow_all = allow_all

    async def async_convert(
        self,
        root: Root,
        value: str,
        param: Optional[click.Parameter],
        ctx: Optional[click.Context],
    ) -> str:
        return value

    async def async_shell_complete(
        self, root: Root, ctx: click.Context, param: click.Parameter, incomplete: str
    ) -> List[CompletionItem]:
        async with AsyncExitStack() as stack:
            client = await stack.enter_async_context(apolo_sdk.get())
            storage: Storage = await stack.enter_async_context(ApiStorage(client))
            runner = await stack.enter_async_context(
                LiveRunner(root.config_dir, root.console, client, storage, root)
            )
            variants = [
                volume.id
                for volume in runner.flow.volumes.values()
                if volume.local is not None
            ]
            if self._allow_all:
                variants += ["ALL"]
        return [
            CompletionItem(image) for image in variants if image.startswith(incomplete)
        ]


LIVE_VOLUME_OR_ALL = LiveVolumeType(allow_all=True)


class BatchType(AsyncType[str]):
    name = "batch"

    def __init__(self, allow_all: bool = False):
        self._allow_all = allow_all

    async def async_convert(
        self,
        root: Root,
        value: str,
        param: Optional[click.Parameter],
        ctx: Optional[click.Context],
    ) -> str:
        return value

    async def async_shell_complete(
        self, root: Root, ctx: click.Context, param: click.Parameter, incomplete: str
    ) -> List[CompletionItem]:
        variants = []
        for file in root.config_dir.config_dir.rglob("*.yml"):
            # We are not trying to parse properly to allow autocompletion of
            # broken yaml files
            if "batch" in file.read_text():
                variants.append(file.stem)
        if self._allow_all:
            variants += ["ALL"]
        return [
            CompletionItem(batch) for batch in variants if batch.startswith(incomplete)
        ]


BATCH = BatchType(allow_all=False)
BATCH_OR_ALL = BatchType(allow_all=True)


class BakeType(AsyncType[str]):
    name = "bake"

    async def async_convert(
        self,
        root: Root,
        value: str,
        param: Optional[click.Parameter],
        ctx: Optional[click.Context],
    ) -> str:
        return value

    async def async_shell_complete(
        self, root: Root, ctx: click.Context, param: click.Parameter, incomplete: str
    ) -> List[CompletionItem]:
        variants = []
        async with AsyncExitStack() as stack:
            client = await stack.enter_async_context(apolo_sdk.get())
            storage: Storage = await stack.enter_async_context(ApiStorage(client))
            runner: BatchRunner = await stack.enter_async_context(
                BatchRunner(root.config_dir, root.console, client, storage, root)
            )
            try:
                async for bake in runner.get_bakes():
                    variants.append(bake.id)
                    if bake.name is not None:
                        variants.append(bake.name)
            except ValueError:
                pass
        return [
            CompletionItem(bake) for bake in variants if bake.startswith(incomplete)
        ]


BAKE = BakeType()


class BakeTaskType(AsyncType[str]):
    name = "task"

    def __init__(
        self,
        *,
        bake_id_param_name: str = "bake_id",
        attempt_no_param_name: str = "bake_id",
        include_started: bool = True,
        include_finished: bool = True,
    ):
        self._bake_id_param_name = bake_id_param_name
        self._attempt_no_param_name = attempt_no_param_name
        self._include_started = include_started
        self._include_finished = include_finished

    async def async_convert(
        self,
        root: Root,
        value: str,
        param: Optional[click.Parameter],
        ctx: Optional[click.Context],
    ) -> str:
        return value

    async def async_shell_complete(
        self, root: Root, ctx: click.Context, param: click.Parameter, incomplete: str
    ) -> List[CompletionItem]:
        variants: List[str] = []
        bake_id = ctx.params[self._bake_id_param_name]
        attempt_no = ctx.params[self._attempt_no_param_name]
        async with AsyncExitStack() as stack:
            client = await stack.enter_async_context(apolo_sdk.get())
            storage: Storage = await stack.enter_async_context(ApiStorage(client))
            runner: BatchRunner = await stack.enter_async_context(
                BatchRunner(root.config_dir, root.console, client, storage, root)
            )
            try:
                bake_id = await resolve_bake(
                    bake_id, project=runner.project_id, storage=storage
                )
                attempt = await runner.get_bake_attempt(bake_id, attempt_no=attempt_no)
            except ResourceNotFound:
                return []
            tasks = [
                task
                async for task in storage.bake(id=bake_id)
                .attempt(id=attempt.id)
                .list_tasks()
            ]
            if self._include_finished:
                variants.extend(
                    ".".join(task.yaml_id) for task in tasks if task.status.is_finished
                )
            if self._include_started:
                variants.extend(
                    ".".join(task.yaml_id) for task in tasks if task.status.is_finished
                )
        return [
            CompletionItem(task) for task in variants if task.startswith(incomplete)
        ]


class ProjectType(AsyncType[str]):
    name = "project"

    async def async_convert(
        self,
        root: Root,
        value: str,
        param: Optional[click.Parameter],
        ctx: Optional[click.Context],
    ) -> str:
        return value

    async def async_shell_complete(
        self, root: Root, ctx: click.Context, param: click.Parameter, incomplete: str
    ) -> List[CompletionItem]:
        variants = []
        async with AsyncExitStack() as stack:
            client = await stack.enter_async_context(apolo_sdk.get())
            storage: Storage = await stack.enter_async_context(ApiStorage(client))
            try:
                async for project in storage.list_projects():
                    variants.append(project.yaml_id)
            except ValueError:
                pass
        return [
            CompletionItem(yaml_id)
            for yaml_id in variants
            if yaml_id.startswith(incomplete)
        ]


PROJECT = ProjectType()
