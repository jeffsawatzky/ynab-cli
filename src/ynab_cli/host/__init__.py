import os

from dotenv import load_dotenv

cwd = os.getcwd()
dot_env_path = os.path.join(cwd, ".env")


def setup_env() -> None:
    if os.path.exists(dot_env_path):
        load_dotenv(dot_env_path)


setup_env()
