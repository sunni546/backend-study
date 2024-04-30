from datetime import datetime, timedelta

import jwt

from config import secret_key

SECRET_KEY = secret_key


def create_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(seconds=60 * 30)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    return token


def validate_token(token):
    try:
        jwt.decode(token, SECRET_KEY, algorithms="HS256")
    except jwt.exceptions.DecodeError:
        return False
    except jwt.exceptions.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False

    return True


def get_user_id(token):
    payload = jwt.decode(token, SECRET_KEY, algorithms="HS256")
    return payload['user_id']
