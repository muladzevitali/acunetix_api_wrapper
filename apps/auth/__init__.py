from functools import wraps

import jwt
from flask import (Blueprint, request, abort)
from flask_restful import Api

from src.config import application_config
from .models import User
from .resources import (Login, AdminLogin)

auth_app = Blueprint(name='auth', import_name=__name__, url_prefix='/auth', template_folder='templates')
auth_app.add_url_rule('admin/login', view_func=AdminLogin.as_view('admin_login'))
auth_api = Api(auth_app)

auth_api.add_resource(Login, '/login')


def auth_required(api_function):
    @wraps(api_function)
    def check_token(*args, **kwargs):
        auth_token = request.headers.get("Authorization")
        if not auth_token:
            abort(401, dict(message='missing token'))
        try:
            payload = jwt.decode(auth_token, application_config.SECRET_KEY)
        except jwt.ExpiredSignatureError:
            return abort(401, dict(message='token expired'))
        except jwt.InvalidTokenError:
            return abort(401, dict(message='invalid token'))

        user = User.query.filter(User.username == payload['username']).first()
        if not user:
            abort(401, dict(message='invalid token'))
        return api_function(*args, **kwargs)

    return check_token
