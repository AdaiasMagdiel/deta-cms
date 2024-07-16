from flask import Blueprint, request
from app.repositories import UniqueException, ValidateException
from app.repositories.role import Role

bp = Blueprint("role", __name__, url_prefix="/role")


@bp.post('')
def register():
    data = request.get_json(silent=True) or {}

    role = Role()
    try:
        role = role.create(data)

    except ValidateException as err:
        return {'error': str(err)}, 422

    except UniqueException as err:
        return {'error': str(err)}, 409

    except Exception:
        import traceback
        traceback.print_exc()

        return {'error': "Unknown error, try again!"}, 500

    return role.to_dict(), 201
