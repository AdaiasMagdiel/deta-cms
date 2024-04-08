from datetime import UTC, datetime
from typing import Any, Optional
from deta import Deta, _Base
from app.entities.common import Repository
from app.entities.user import UserModel
from werkzeug.security import generate_password_hash


class UserRepository(Repository):
    _deta: Deta
    _base: _Base

    table = 'users'

    def create(self, data: dict[str, Any]) -> UserModel:
        now = datetime.now(UTC)

        data['created_at'] = now.isoformat()
        data['updated_at'] = now.isoformat()

        if 'key' not in data:
            data['key'] = None

        if 'password' in data:
            data['password'] = generate_password_hash(data['password'])

        by_username = self.get_by('username', data.get('username', ''))
        if by_username is not None:
            raise ValueError('The provided username is already in use.')

        by_email = self.get_by('email', data.get('email', ''))
        if by_email is not None:
            raise ValueError('The provided email is already in use.')

        user = UserModel(**data)

        res = self._base.put(user.model_dump())
        user.key = res['key']

        return user

    def get_by(self, key: str, value: str) -> Optional[UserModel]:
        res = self._base.fetch({key: value})

        if res.count == 0:
            return None

        user = res.items[0]
        return UserModel(**user)
