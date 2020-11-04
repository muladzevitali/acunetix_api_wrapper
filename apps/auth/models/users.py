from datetime import (datetime, timedelta)
from hashlib import sha256
from typing import (Union)

import jwt
from flask_login import (AnonymousUserMixin, login_user)
from flask_security import (UserMixin)
from sqlalchemy.ext.hybrid import hybrid_property

from apps import db
from src.config import (database, application_config)

table_prefix = database.table_prefix


class User(db.Model):
    __tablename__ = f'{table_prefix}_users'

    id = db.Column(db.Integer, db.Sequence(f'{table_prefix}_users_id_seq', start=10000), primary_key=True)
    authenticated = db.Column(db.Boolean(), default=0)
    active = db.Column(db.Boolean(), default=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50))
    _password = db.Column(db.String(64), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)

    def save(self):
        """Insert user into database"""
        db.session.add(self)
        db.session.commit()

    @hybrid_property
    def password(self):
        """Return the hashed user password."""
        return self._password

    @password.setter
    def password(self, new_pass):
        """Hash and save the user's new password."""
        password_hash = self.hash_password(new_pass)
        self._password = password_hash

    @staticmethod
    def hash_password(password: str) -> hex:
        """Password hashing handler"""
        return sha256(password.encode()).hexdigest()

    def get_id(self):
        return self.username

    def login(self):
        self.authenticated = True
        login_user(self, remember=True)
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id_: int) -> 'User':
        """Get user by id"""
        user: 'User' = User.query.filter(User.id == id_).first()

        return user

    def encode_auth_token(self) -> Union[bytes, str]:
        """
        Generates the Auth Token
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=5000, seconds=0),
                'iat': datetime.utcnow(),
                'username': self.username
            }
            return jwt.encode(
                payload,
                application_config.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return str(e)

    @staticmethod
    def decode_auth_token(auth_token) -> str:
        """
        Decode auth token provided from request
        """
        try:
            payload = jwt.decode(auth_token, application_config.SECRET_KEY, )
            return payload['username']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return self.active

    def __repr__(self):
        return '%s' % self.username

    def __str__(self):
        return '%s' % self.username


class AnonymousUser(AnonymousUserMixin, UserMixin):
    def __init__(self):
        self.username = "Anonymous"
        self.email = "anonymous@bog.ge"
        self.authenticated = False
        self.id = -1
        self.is_anonymous = True
        self.password = "anonymous"
        self.active = False
        self.is_admin = False

    def get_user_id(self):
        return self.id

    def has_role(self, role):
        return False

    def is_anonymous(self):
        return True
