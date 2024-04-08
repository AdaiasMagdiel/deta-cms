from deta import Deta
from app.settings import settings


class Repository:
    table: str

    def __init__(self) -> None:
        self._deta = Deta(project_key=settings.DETA_PROJECT_KEY)
        self._base = self._deta.Base(self.table)
