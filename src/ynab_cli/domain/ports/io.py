from getpass import getpass
from io import BytesIO
from typing import Protocol

from PIL import Image
from typing_extensions import override


class IO(Protocol):
    async def prompt(self, prompt: str, password: bool = False) -> str: ...

    async def print(self, message: str) -> None: ...

    async def display_image(self, image: BytesIO) -> None: ...


class StdinIO(IO):
    @override
    async def prompt(self, prompt: str, password: bool = False) -> str:
        if password:
            return getpass(prompt)
        else:
            return input(prompt)

    @override
    async def print(self, message: str) -> None:
        print(message)

    @override
    async def display_image(self, image: BytesIO) -> None:
        img = Image.open(image)
        img.show()
