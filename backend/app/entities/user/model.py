from typing import Optional
from pydantic import BaseModel


class UserModel(BaseModel):
    key: Optional[str]
    name: str
    username: str
    email: str
    password: str
    role: str
    created_at: str
    updated_at: str
