# backported from cpython 3.12 bceb197947bbaebb11e01195bdce4f240fdf9332
# Copyright © 2001-2022 Python Software Foundation; All Rights Reserved
# modified to support working on 3.10 (basically just the imports changed here)

import collections.abc
import contextlib
import enum
import sys
from types import TracebackType
from typing import Union, final, Optional, Type

from asyncio import events
from asyncio import exceptions
from asyncio import tasks
from . import install as _install

from typing_extensions import Self

__all__ = (
    "Timeout",
    "timeout",
    "timeout_at",
)


class _State(enum.Enum):
    CREATED = "created"
    ENTERED = "active"
    EXPIRING = "expiring"
    EXPIRED = "expired"
    EXITED = "finished"


@final
class Timeout:
    def __init__(self, when: Optional[float]) -> None:
        self._state = _State.CREATED

        self._timeout_handler: Optional[Union[events.TimerHandle, events.Handle]] = None
        self._task: Optional[tasks.Task] = None
        self._when = when
        self._cmgr = self._cmgr_factory()

    def when(self) -> Optional[float]:
        return self._when

    def reschedule(self, when: Optional[float]) -> None:
        assert self._state is not _State.CREATED
        if self._state is not _State.ENTERED:
            raise RuntimeError(
                f"Cannot change state of {self._state.value} Timeout",
            )

        self._when = when

        if self._timeout_handler is not None:
            self._timeout_handler.cancel()

        if when is None:
            self._timeout_handler = None
        else:
            loop = events.get_running_loop()
            if when <= loop.time():
                self._timeout_handler = loop.call_soon(self._on_timeout)
            else:
                self._timeout_handler = loop.call_at(when, self._on_timeout)

    def expired(self) -> bool:
        """Is timeout expired during execution?"""
        return self._state in (_State.EXPIRING, _State.EXPIRED)

    def __repr__(self) -> str:
        info = [""]
        if self._state is _State.ENTERED:
            when = round(self._when, 3) if self._when is not None else None
            info.append(f"when={when}")
        info_str = " ".join(info)
        return f"<Timeout [{self._state.value}]{info_str}>"

    @contextlib.asynccontextmanager
    async def _cmgr_factory(self) -> collections.abc.AsyncGenerator[Self, None]:
        self._state = _State.ENTERED
        async with _install.install_uncancel():
            self._task = tasks.current_task()
            if self._task is None:
                raise RuntimeError("Timeout should be used inside a task")
            self._cancelling = self._task.cancelling()
            self.reschedule(self._when)
            try:
                yield self
            finally:
                exc_type, exc_value, _ = sys.exc_info()
                assert self._state in (_State.ENTERED, _State.EXPIRING)

                if self._timeout_handler is not None:
                    self._timeout_handler.cancel()
                    self._timeout_handler = None

                if self._state is _State.EXPIRING:
                    self._state = _State.EXPIRED

                    if (
                        self._task.uncancel() <= self._cancelling
                        and exc_type is exceptions.CancelledError
                    ):
                        # Since there are no outstanding cancel requests, we're
                        # handling this.
                        raise TimeoutError from exc_value
                elif self._state is _State.ENTERED:
                    self._state = _State.EXITED

    async def __aenter__(self) -> "Timeout":
        return await self._cmgr.__aenter__()

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> Optional[bool]:
        return await self._cmgr.__aexit__(exc_type, exc_val, exc_tb)

    def _on_timeout(self) -> None:
        assert self._state is _State.ENTERED
        assert self._task is not None
        self._task.cancel()
        self._state = _State.EXPIRING
        # drop the reference early
        self._timeout_handler = None


def timeout(delay: Optional[float]) -> Timeout:
    """Timeout async context manager.

    Useful in cases when you want to apply timeout logic around block
    of code or in cases when asyncio.wait_for is not suitable. For example:

    >>> async with asyncio.timeout(10):  # 10 seconds timeout
    ...     await long_running_task()


    delay - value in seconds or None to disable timeout logic

    long_running_task() is interrupted by raising asyncio.CancelledError,
    the top-most affected timeout() context manager converts CancelledError
    into TimeoutError.
    """
    loop = events.get_running_loop()
    return Timeout(loop.time() + delay if delay is not None else None)


def timeout_at(when: Optional[float]) -> Timeout:
    """Schedule the timeout at absolute time.

    Like timeout() but argument gives absolute time in the same clock system
    as loop.time().

    Please note: it is not POSIX time but a time with
    undefined starting base, e.g. the time of the system power on.

    >>> async with asyncio.timeout_at(loop.time() + 10):
    ...     await long_running_task()


    when - a deadline when timeout occurs or None to disable timeout logic

    long_running_task() is interrupted by raising asyncio.CancelledError,
    the top-most affected timeout() context manager converts CancelledError
    into TimeoutError.
    """
    return Timeout(when)
