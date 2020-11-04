from flask_testing import TestCase

from apps import (app, db)


class BaseTestCase(TestCase):
    """A base test case for flask-tracking."""

    def create_app(self):
        db.create_all()
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self) -> None:
        db.session.rollback()
        db.drop_all()