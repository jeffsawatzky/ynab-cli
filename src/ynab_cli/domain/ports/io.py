from getpass import getpass
from typing import Protocol

from typing_extensions import override


class Progress(Protocol):
    async def update(
        self, *, total: float | None = None, completed: float | None = None, advance: float | None = None
    ) -> None: ...


class IO(Protocol):
    progress: Progress

    async def prompt(self, prompt: str, password: bool = False) -> str: ...

    async def print(self, message: str) -> None: ...


class StdProgress(Progress):
    def __init__(self, io: "StdIO") -> None:
        self._io = io
        self._total: float | None = None
        self._completed: float | None = None

    @override
    async def update(
        self, *, total: float | None = None, completed: float | None = None, advance: float | None = None
    ) -> None:
        if total is not None:
            self._total = total
        if completed is not None:
            self._completed = completed
        if advance is not None:
            if self._completed is None:
                self._completed = 0
            self._completed += advance

        if self._total is not None and self._completed is not None:
            await self._io.print(f"Progress: {self._completed}/{self._total}")
        elif self._total is not None:
            await self._io.print(f"Progress: {self._total} to go")
        elif self._completed is not None:
            await self._io.print(f"Progress: {self._completed} completed")
        else:
            await self._io.print("No progress information available")


class StdIO(IO):
    def __init__(self) -> None:
        self.progress = StdProgress(self)

    @override
    async def prompt(self, prompt: str, password: bool = False) -> str:
        if password:
            return getpass(prompt)
        else:
            return input(prompt)

    @override
    async def print(self, message: str) -> None:
        print(message)
