from typing import Optional
from deta import _Base
from app.repositories import Repository
from app.utils import slugify


class Role:
    base: _Base
    table: str = "roles"
    ready: bool = False
    fields: tuple = ('key', 'value', 'slug')

    def __init__(
        self,
        key: Optional[str] = None,
        value: Optional[str] = None,
        slug: Optional[str] = None,
    ):
        self.key = key
        self.value = value
        if slug is None:
            self.slug = slugify(value)

        self.init_db()

    @classmethod
    def init_db(cls):
        if cls.ready is False:
            cls.base = Repository.get_deta().Base(cls.table)
            cls.ready = True

        return cls

    def insert(self, data: dict[str, str]) -> 'Role':
        for k, v in data.items():
            if k in self.fields:
                setattr(self, k, v)

        if 'slug' not in data:
            self.slug = slugify(self.value)

        res: dict = self.base.put(self.to_dict())  #type:ignore
        self.key = res['key']

        return self

    def to_dict(self) -> dict:
        return {
            k: v
            for k, v in self.__dict__.items()
            if not callable(v) and not k.startswith('__') and k in self.fields
        }
