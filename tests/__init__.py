import os


def fixture_exists(fixture_path: str) -> bool:
    """Check if a fixture file exists."""

    return os.path.isfile(os.path.join("tests", "fixtures", fixture_path))


def load_fixture(fixture_path: str) -> str:
    """Load a fixture file."""

    with open(os.path.join("tests", "fixtures", fixture_path), encoding="utf-8") as file:
        return file.read()
