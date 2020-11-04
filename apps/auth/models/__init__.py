from flask import (redirect, url_for, session)
from flask_login import current_user

from .users import (User, AnonymousUser)


def user_loader(username):
    """User loader for flask login"""
    return User.query.filter_by(username=username).first()


def unauthorized():
    """Unauthorized handler for flask_login"""
    if not current_user.authenticated:
        return redirect(url_for("auth.admin_login"))

    return redirect(session["next_url"] or url_for("admin.index"))
