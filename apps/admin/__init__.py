from flask_admin import Admin

from apps import db
from apps.auth.models import User
from .model_views import (IndexView, UserView)

admin_app = Admin(endpoint='admin', index_view=IndexView(url="/admin"), template_mode='bootstrap3')
admin_app.add_view(UserView(User, db.session, name='Users'))
