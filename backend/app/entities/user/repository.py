from datetime import UTC, datetime
from typing import Any, Optional
from deta import Deta, _Base
from werkzeug.security import generate_password_hash
from app.entities.common import Repository
from app.entities.user import UserModel
from app.entities.user.exceptions import NotFoundException


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

        if 'username' in data:
            data['username'] = data['username'].lower()

        if 'email' in data:
            data['email'] = data['email'].lower()

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

    def update(self, user_key: str, data: dict[str, Any]) -> UserModel:
        if 'key' in data:
            del data['key']

        data['updated_at'] = datetime.now(UTC).isoformat()

        if 'username' in data:
            data['username'] = data['username'].lower()

        if 'email' in data:
            data['email'] = data['email'].lower()

        by_username = self.get_by('username', data.get('username', ''))
        if by_username is not None:
            raise ValueError('The provided username is already in use.')

        by_email = self.get_by('email', data.get('email', ''))
        if by_email is not None:
            raise ValueError('The provided email is already in use.')

        user = self.get_by('key', user_key)
        if user is None:
            raise NotFoundException(f'There\'s no user with "{user_key}" key.')

        user.update(**data)

        self._base.update(data, key=user_key)
        return user

    def get_by(self, key: str, value: str) -> Optional[UserModel]:
        res = self._base.fetch({key: value})

        if res.count == 0:
            return None

        user = res.items[0]
        return UserModel(**user)

    def get_all(self, page: int, per_page: int) -> list[UserModel]:
        items = []
        last = None

        for i in range(page):
            res = self._base.fetch(limit=per_page, last=last)
            items = res.items
            last = res.last
            if last is None:
                break

        return [UserModel(**data) for data in items]

    def delete(self, user_key: str) -> None:
        user = self.get_by('key', user_key)
        if user is None:
            raise NotFoundException(f'There\'s no user with "{user_key}" key.')

        self._base.delete(user_key)
