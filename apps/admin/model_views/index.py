from flask import (redirect, url_for, request, session)
from flask_admin import AdminIndexView
from flask_login import (current_user)


class IndexView(AdminIndexView):
    """Class For Home admin page models"""

    def is_accessible(self):
        return current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page i  f user doesn't have access
        session["next_url"] = request.endpoint
        return redirect(url_for('auth.admin_login'))
