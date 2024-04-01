from flask import Blueprint

bp = Blueprint("routes", __name__)


@bp.get("/")
def index():
    return {"message": "Hello World"}
