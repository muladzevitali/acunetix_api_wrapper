from flask import (session, request, redirect, url_for)
from flask_admin.babel import gettext
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class UserView(ModelView):
    """Class for Admin models view"""
    can_delete = False
    column_list = ('username', 'email', 'is_admin')
    form_columns = ('username', 'email', 'is_admin', 'password')

    def is_accessible(self):
        if current_user.is_admin:
            return True

        return False

    def inaccessible_callback(self, name, **kwargs):
        session["next_url"] = request.endpoint

        return redirect(url_for('auth.admin_login'))

    def get_empty_list_message(self):
        return gettext('No User found')
