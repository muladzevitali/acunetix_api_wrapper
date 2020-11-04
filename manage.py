import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from apps import (create_app, db)
from apps.auth.models import User
from src.config import (application_config, admin_user)

application = create_app(application_config)
tables = [User.__table__, ]
migrate = Migrate(application, db, max_identifier_length=128)

manager = Manager(application)
manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    with application.app_context():
        db.metadata.create_all(db.engine, tables=tables)
        user = User()
        user.email = admin_user.email
        user.username = admin_user.username
        user.password = admin_user.password
        user.is_admin = admin_user.is_admin
        user.active = True
        user.save()


@manager.command
def reset_db():
    with application.app_context():
        db.metadata.drop_all(db.engine, tables=tables)
        create_db()


@manager.command
def test():
    """Run unit tests."""
    tests = unittest.TestLoader().discover('tests', pattern='*.py')
    unittest.TextTestRunner(verbosity=1).run(tests)


@manager.command
def runserver():
    application.run(host='0.0.0.0', port='6009', debug=True)


if __name__ == '__main__':
    manager.run()
