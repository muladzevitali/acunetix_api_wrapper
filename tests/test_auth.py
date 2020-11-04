import json
import unittest

from apps.auth.models import User
from tests.base import BaseTestCase


class TestAuthBlueprint(BaseTestCase):
    def test_registered_user_login(self):
        """ Test for login of registered-user login """
        with self.client:
            user = User(email='test@test.com', password='test', username='test', is_admin=False)
            user.save()
            # registered user login
            response = self.client.post('/auth/login', data=dict(username='test', password='test'))
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_non_registered_user_login(self):
        """ Test for login of non-registered user """
        with self.client:
            response = self.client.post('/auth/login', data=dict(username='john', password='123456'))
            self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
