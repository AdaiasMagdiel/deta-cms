from typing import Optional
from deta import _Base
from app.repositories import Base, UniqueException, ValidateException
from app.utils import slugify


class Role(Base):
    base: _Base
    table: str = "roles"
    ready: bool = False
    fields: tuple = ('key', 'title', 'slug')

    def __init__(
        self,
        key: Optional[str] = None,
        title: Optional[str] = None,
        slug: Optional[str] = None,
    ):
        self.key = key
        self.title = title

        if slug is None:
            self.slug = slugify(title or "")
        else:
            self.slug = slug

        self.init_db()

    def validate(self,
                 data: dict[str, str],
                 required: list[str] = []) -> dict[str, str]:
        data = {k: v for k, v in data.items() if k in self.fields}

        for k in required:
            if k not in data or not data[k]:
                raise ValidateException(f"The field '{k}' is required.")

        if data['title'] == '':
            raise ValidateException("The 'title' should be not empty.")

        if 'title' in data and ('slug' not in data or data['slug'] == ''):
            data['slug'] = slugify(data['title'])

        return data

    def get_by(self, key: str, value: str) -> Optional['Role']:
        return super().base_get_by(key, value, Role)

    def create(self, data: dict[str, str]) -> 'Role':
        data = self.validate(data, required=['title'])

        exists = self.get_by('slug', slugify(data['title']))
        if exists:
            raise UniqueException(
                "Already exist a role with title '{0}'.".format(data['title'])
            )

        exists = self.get_by('slug', data['slug'])
        if exists:
            raise UniqueException(
                "Already exists a role with slug '{0}'.".format(data['slug'])
            )

        for k, v in data.items():
            if k in self.fields:
                setattr(self, k, v)

        res: dict = self.base.put(self.to_dict())  # type:ignore
        self.key = res['key']

        return self
