import string
from typing import Optional
from pydantic import field_validator
from app.entities.common import Model


class UserModel(Model):
    key: Optional[str]
    name: str
    username: str
    email: str
    password: str
    role: str
    created_at: str
    updated_at: str

    @field_validator('email')
    @classmethod
    def validate_email(cls, value: str) -> str:
        if '@' not in value:
            raise ValueError("Invalid email format")

        if '.' not in value.split('@')[-1]:
            raise ValueError("Invalid email format")

        return value

    @field_validator('username')
    @classmethod
    def validate_username(cls, value: str) -> str:
        valid = string.ascii_letters + string.digits + '_-.'

        for char in value:
            if char not in valid:
                raise ValueError(
                    'Invalid username, the username should contain only letters, numbers and this digits: "_", "-" and "."'
                )

        return value
