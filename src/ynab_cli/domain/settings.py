from pydantic import BaseModel


class YnabSettings(BaseModel):
    access_token: str = ""
    budget_id: str = ""


class AmazonSettings(BaseModel):
    username: str = ""
    password: str = ""
    host: str = ""


class Settings(BaseModel):
    dry_run: bool = False

    ynab: YnabSettings = YnabSettings()
    amazon: AmazonSettings | None = None
