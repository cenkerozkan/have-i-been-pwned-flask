from pydantic import BaseModel

class HibpBreachedAccountModel(BaseModel):
    domain: str
    title: str
    breach_date: str
    description: str
    is_verified: bool