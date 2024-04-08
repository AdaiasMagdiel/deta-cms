from flask import Blueprint, request
from pydantic import ValidationError
from app.entities.user import UserRepository
from app.entities.user.model import UserModel

bp = Blueprint("users", __name__, url_prefix='/users')


@bp.post("")
def index():
    data = request.get_json(silent=True) or {}

    try:
        repo = UserRepository()
        user: UserModel = repo.create(data)

        return {"user": user.model_dump(exclude={'password'})}, 201
    except ValidationError as e:
        return {
            'error':
                'Missing fields',
            'errors':
                e.errors(
                    include_context=False,
                    include_input=False,
                    include_url=False
                )
        }, 422
    except ValueError as e:
        return {'error': str(e)}, 422
