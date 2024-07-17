import re
from typing import Any, Optional
from deta import _Base
from app.repositories import Base, UniqueException, ValidateException
from app.repositories.role import Role
from app.utils import slugify


class User(Base):
    base: _Base
    table: str = "users"
    ready: bool = False
    fields: tuple = ('key', 'email', 'name', 'username', 'password', 'role')

    def __init__(
        self,
        key: Optional[str] = None,
        email: Optional[str] = None,
        name: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        role: Optional[str] = None
    ):
        self.key = key
        self.email = email
        self.name = name
        self.username = username
        self.password = password
        self.role = role

        self.init_db()

    def validate(self,
                 data: dict[str, str],
                 required: list[str] = []) -> dict[str, str]:
        data = {k: v for k, v in data.items() if k in self.fields}

        if 'email' in data:
            data['email'] = data['email'].lower()

        for k in required:
            if k not in data or not data[k]:
                raise ValidateException(f"The field '{k}' is required.")

        # Name and username should have at least 3 characters
        if 'name' in data and len(data['name']) < 3:
            raise ValidateException(
                "The field 'name' should be at least 3 characters long."
            )

        if 'username' in data and len(data['username']) < 3:
            raise ValidateException(
                "The field 'username' should be at least 3 characters long."
            )

        # Email should be a valid email format
        if 'email' in data and not re.match(
            r"[^@]+@[^@]+\.[^@]+", data['email']
        ):
            raise ValidateException(
                "The field 'email' should be a valid email address."
            )

        # Username should only contain letters, digits, dot, underscore, or hyphen
        if 'username' in data and not re.match(
            r"^[a-zA-Z0-9._-]+$", data['username']
        ):
            raise ValidateException(
                "The field 'username' should only contain letters, digits, dot, underscore, or hyphen."
            )

        return data

    def get_by(self, key: str, value: str) -> Optional['User']:
        return super().base_get_by(key, value, User)

    def get_role(self) -> Optional[Role]:
        return Role().get_by('slug', self.role)

    def to_dict(self, hide: list[str] = []) -> dict:
        data = super().to_dict(hide=hide)
        role = self.get_role()

        if role is not None:
            data['role'] = role.to_dict()

        return data

    def create(self, data: dict[str, str]) -> 'User':
        data = self.validate(
            data, required=['name', 'username', 'email', 'password', 'role']
        )

        exists = self.get_by('username', data['username'].lower())
        if exists:
            raise UniqueException(
                "The username '{0}' is already taken.".format(data['username'])
            )

        exists = self.get_by('email', data['email'].lower())
        if exists:
            raise UniqueException(
                "The email '{0}' is already registered.".format(data['email'])
            )

        role_repo = Role()

        role = role_repo.get_by('slug', slugify(data['role']))
        if role is None:
            role = role_repo.create({'title': data['role']})

        del data['role']

        for k, v in data.items():
            setattr(self, k, v)

        self.role = role.slug

        res: dict = self.base.put(self.to_dict())  # type: ignore
        self.key = res['key']

        return self
