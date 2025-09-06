from pydantic import BaseModel


class CreateNewUserModel(BaseModel):
    user_name: str
    email: str
    password: str


class UserCredentials(BaseModel):
    email: str
    password: str


class ChangePasswordModel(BaseModel):
    user_name: str
    password: str