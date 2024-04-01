from flask import Flask
from app.settings import settings
from app.cache import cache
from app.routes import Router


def create_app() -> Flask:
    app = Flask(__name__)

    settings.init_app(app)
    cache.init(settings.DETA_KEY, settings.CACHE_TABLE)
    Router.init_app(app)

    return app
