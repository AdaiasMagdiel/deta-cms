from flask import Flask
from app.settings import settings
from app.cache import cache


def create_app() -> Flask:
    app = Flask(__name__)

    settings.init_app(app)
    cache.init(
        deta_key=settings.DETA_PROJECT_KEY, table_name=settings.CACHE_TABLE
    )

    return app
