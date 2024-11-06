from pydantic import BaseModel


class Form(BaseModel):
    action: str
    method: str
    data: dict[str, str]
