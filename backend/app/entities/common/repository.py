from deta import Deta
from app.settings import settings


class Repository:
    table: str

    def __init__(self) -> None:
        self._deta = Deta(project_key=settings.DETA_PROJECT_KEY)
        self._base = self._deta.Base(self.table)

    def drop(self):
        res = self._base.fetch()
        all_items = res.items

        while res.last:
            res = self._base.fetch(last=res.last)
            all_items += res.items

        for item in all_items:
            self._base.delete(item['key'])
