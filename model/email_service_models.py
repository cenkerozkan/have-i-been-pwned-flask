from pydantic import BaseModel


class NewEmailModel(BaseModel):
    email: str
