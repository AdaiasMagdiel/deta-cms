from datetime import UTC, datetime
from typing import Any
from deta import Deta, _Base
from app.entities.common import Repository
from app.entities.user import UserModel


class UserRepository(Repository):
    _deta: Deta
    _base: _Base

    table = 'users'

    def create(self, data: dict[str, Any]) -> UserModel:
        now = datetime.now(UTC)

        data['key'] = None
        data['created_at'] = now.isoformat()
        data['updated_at'] = now.isoformat()

        user = UserModel(**data)

        res = self._base.put(user.model_dump())
        user.key = res['key']

        return user
