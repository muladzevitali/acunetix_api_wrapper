from flask import (render_template, redirect, request, url_for)
from flask_login import login_user, current_user
from flask.views import MethodView

from ..models import User


class AdminLogin(MethodView):
    def get(self):
        if current_user.is_authenticated and current_user.is_admin:
            return redirect(url_for('admin.index'))
        return render_template('login.html')

    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')
        if not (username and password):
            return redirect(url_for('auth.admin_login'))

        user = User.query.filter(User.username == username).first()
        if not user:
            return redirect(url_for('auth.admin_login'))

        if not (user.password == User.hash_password(request.form.get('password')) and user.is_admin):
            return redirect(url_for('auth.admin_login'))

        user.login()

        return redirect(url_for('admin.index'))
