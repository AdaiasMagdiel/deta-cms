import jwt
import datetime
from flask import Blueprint, request
from app.repositories import UniqueException, ValidateException
from app.settings import settings
from app.repositories.user import User

bp = Blueprint("auth", __name__, url_prefix="/auth")


def generate_token(user_id):
    payload = {
        'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1),
        'iat': datetime.datetime.now(datetime.UTC),
        'sub': user_id
    }
    token = jwt.encode(payload, settings.FLASK_SECRET_KEY, algorithm='HS256')
    return token


@bp.post('/register')
def register():
    data = request.get_json(silent=True) or {}

    user = User()
    try:
        user = user.create(data)

    except ValidateException as err:
        return {'error': str(err)}, 422

    except UniqueException as err:
        return {'error': str(err)}, 409

    except Exception:
        import traceback
        traceback.print_exc()

        return {'error': "Unknown error, try again!"}, 500

    token = generate_token(user.key)

    return {"token": token, "user": user.to_dict(hide=['password'])}, 201
