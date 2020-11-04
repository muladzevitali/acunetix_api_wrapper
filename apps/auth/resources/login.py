from flask import request
from flask_restful import (Resource)

from ..models import User


class Login(Resource):
    def post(self):
        if not (request.form.get('username') and request.form.get('password')):
            return {'message': 'please provide username and password to login'}, 400

        user = User.query.filter(User.username == request.form.get('username')).first()
        if not user:
            return {'message': 'please provide valid credentials'}, 401

        if not user.password == User.hash_password(request.form.get('password')):
            return {'message': 'please provide valid credentials'}, 401

        auth_token = user.encode_auth_token()

        return {'status': 'success', 'auth_token': auth_token.decode()}, 200
