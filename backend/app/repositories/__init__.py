from typing import Any, Optional, Type, TypeVar
from deta import Deta, _Base
from app.settings import settings

T = TypeVar('T')


class Repository:
    deta: Deta
    ready: bool = False

    @classmethod
    def get_deta(cls):
        if cls.ready is False:
            cls.deta = Deta(settings.DETA_PROJECT_KEY)
            cls.ready = True

        return cls.deta


class Base:
    base: _Base
    table: str
    ready: bool
    fields: tuple

    @classmethod
    def init_db(cls):
        if cls.ready is False:
            cls.base = Repository.get_deta().Base(cls.table)
            cls.ready = True

        return cls

    def get(self, key: str):
        return self.base.get(key)

    def count(self) -> int:
        res = self.base.fetch()
        count = res.count

        while res.last:
            res = self.base.fetch(last=res.last)
            count += res.count

        return count

    def base_get_by(self, key: str, value: Any,
                    base_class: Type[T]) -> Optional[T]:
        res = self.base.fetch({key: value})

        if res.count == 0:
            return None

        instance = base_class(**res.items[0])
        return instance

    def to_dict(self, hide: list[str] = []) -> dict:
        return {
            k: v
            for k, v in self.__dict__.items()
            if k in self.fields and k not in hide
        }

    def drop_all(self):
        res = self.base.fetch()
        all_items = res.items

        while res.last:
            res = self.base.fetch(last=res.last)
            all_items += res.items

        for item in all_items:
            self.base.delete(item['key'])

    def __repr__(self) -> str:
        template = "<{name} {params}>"
        name = self.__class__.__name__

        params = []
        for key, value in self.to_dict().items():
            params.append(f'{key}="{value}"')

        template = template.format(name=name, params=" ".join(params))

        return template


class ValidateException(Exception):
    pass


class UniqueException(Exception):
    pass
