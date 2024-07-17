from flask import Blueprint
from . import auth, role

bp = Blueprint("api", __name__, url_prefix="/api")


def init_router(main: Blueprint):
    bp.register_blueprint(auth.bp)
    bp.register_blueprint(role.bp)

    main.register_blueprint(bp)
