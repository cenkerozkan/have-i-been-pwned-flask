from pydantic import BaseModel, EmailStr

class EmailStrTest(BaseModel):
    email: EmailStr
    password: str


if __name__ == '__main__':
    obj = EmailStrTest(email="email@email.com", password="password")
    print(obj.model_dump())