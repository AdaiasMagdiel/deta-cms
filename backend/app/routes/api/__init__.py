from flask import Blueprint
from . import auth

bp = Blueprint("api", __name__, url_prefix="/api")


def init_router(main: Blueprint):
    bp.register_blueprint(auth.bp)

    main.register_blueprint(bp)
