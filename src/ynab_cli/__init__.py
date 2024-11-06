from os.path import dirname, join

from dotenv import load_dotenv


def setup_env() -> None:
    dotenv_path = join(dirname(__file__), "..", "..", ".env")
    load_dotenv(dotenv_path)


setup_env()
