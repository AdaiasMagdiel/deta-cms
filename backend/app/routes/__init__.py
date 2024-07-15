from flask import Blueprint, Flask
from . import api

bp = Blueprint("routes", __name__)


def Router(app: Flask):
    for inner_bp in [api]:
        inner_bp.init_router(bp)

    app.register_blueprint(bp)
