import os
from pathlib import Path

BASE_PATH = os.path.dirname(__file__)


def fixture_exists(path: str) -> bool:
    p = Path(BASE_PATH) / Path("fixtures") / Path(path)
    return p.exists()


def load_fixture(path: str) -> str:
    p = Path(BASE_PATH) / Path("fixtures") / Path(path)
    with p.open() as f:
        return f.read()
