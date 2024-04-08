from flask import Blueprint, Flask
from app.routes.api import users

api = Blueprint("api", __name__, url_prefix="/api")


class Api:
    def __init__(self, app: Flask) -> None:
        api.register_blueprint(users.bp)
        app.register_blueprint(api)
