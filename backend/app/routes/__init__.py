from flask import Flask
from app.routes.api import Api


class Router:
    @classmethod
    def init_app(cls, app: Flask) -> None:
        Api(app)
