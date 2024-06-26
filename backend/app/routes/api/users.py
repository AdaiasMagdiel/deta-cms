from flask import Blueprint, request
from pydantic import ValidationError
from app.entities.user import UserRepository
from app.entities.user.exceptions import NotFoundException
from app.entities.user.model import UserModel

bp = Blueprint("users", __name__, url_prefix='/users')


@bp.post("")
def create():
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


@bp.get("")
def get_all():
    page = request.args.get('page', 1, int)
    per_page = request.args.get('per_page', 20, int)

    repo = UserRepository()
    users = repo.get_all(page, per_page)

    return {
        'last_page': len(users) == 0 or len(users) < per_page,
        'page': page,
        'per_page': page,
        'users': [user.model_dump(exclude={'password'}) for user in users]
    }


@bp.get("/<user_key>")
def get(user_key: str):
    repo = UserRepository()
    user: UserModel = repo.get_by('key', user_key)

    if user is None:
        return {'error': 'User not found'}, 404

    return {"user": user.model_dump(exclude={'password'})}, 200


@bp.put("/<user_key>")
def update(user_key: str):
    data = request.get_json(silent=True) or {}

    try:
        repo = UserRepository()
        user: UserModel = repo.update(user_key, data)

        return user.model_dump(exclude={'password'}), 200
    except ValidationError as e:
        return {
            'error':
                'Validation Error',
            'errors':
                e.errors(
                    include_context=False,
                    include_input=False,
                    include_url=False
                )
        }, 422
    except ValueError as e:
        return {'error': str(e)}, 422
    except NotFoundException as e:
        return {'error': str(e)}, 404


@bp.delete("/<user_key>")
def delete(user_key: str):
    try:
        repo = UserRepository()
        repo.delete(user_key)

        return {'status': 'success'}, 200
    except NotFoundException as e:
        return {'error': str(e)}, 404
