from __future__ import annotations

from asyncio import TaskGroup, run
from collections.abc import Callable
from dataclasses import dataclass
from functools import partial
from inspect import iscoroutinefunction
from logging import getLogger
from sys import version_info
from typing import TYPE_CHECKING, cast

from typing_extensions import override

from utilities.asyncio import Coroutine1
from utilities.logging import LoggerOrName, get_logger

if TYPE_CHECKING:
    from collections.abc import Iterable
    from types import TracebackType

    from utilities.asyncio import MaybeCoroutine1
    from utilities.types import StrMapping

_LOGGER = getLogger(__name__)
VERSION_MAJOR_MINOR = (version_info.major, version_info.minor)


def make_except_hook(
    *,
    logger: LoggerOrName = _LOGGER,
    message: object = "",
    extra: StrMapping | None = None,
    callbacks: Iterable[Callable[[], MaybeCoroutine1[None]]] | None = None,
) -> Callable[
    [type[BaseException] | None, BaseException | None, TracebackType | None], None
]:
    """Create an exception hook with various features."""
    return partial(
        _make_except_hook_inner,
        logger=logger,
        message=message,
        extra=extra,
        callbacks=callbacks,
    )


def _make_except_hook_inner(
    exc_type: type[BaseException] | None,
    exc_val: BaseException | None,
    traceback: TracebackType | None,
    /,
    *,
    logger: LoggerOrName = _LOGGER,
    message: object = "",
    extra: StrMapping | None = None,
    callbacks: Iterable[Callable[[], MaybeCoroutine1[None]]] | None = None,
) -> None:
    """Exception hook to log the traceback."""
    _ = (exc_type, traceback)
    if exc_val is None:
        raise MakeExceptHookError
    logger_use = get_logger(logger)
    logger_use.exception(message, extra=extra)
    async_callbacks: list[Callable[[], Coroutine1[None]]] = []
    if callbacks is not None:
        for callback in callbacks:
            if not iscoroutinefunction(callback):
                cast(Callable[[], None], callback)()
            else:  # skipif-ci
                async_callback = cast(Callable[[], Coroutine1[None]], callback)
                async_callbacks.append(async_callback)
    if len(async_callbacks) >= 1:  # skipif-ci
        run(_run_async_callbacks(async_callbacks))


@dataclass(kw_only=True, slots=True)
class MakeExceptHookError(Exception):
    @override
    def __str__(self) -> str:
        return "No exception to log"


async def _run_async_callbacks(
    callbacks: Iterable[Callable[[], Coroutine1[None]]], /
) -> None:
    """Run all asynchronous callbacks."""
    async with TaskGroup() as tg:  # skipif-ci
        for callback in callbacks:
            _ = tg.create_task(callback())


__all__ = ["VERSION_MAJOR_MINOR", "MakeExceptHookError", "make_except_hook"]
