import json
import unittest

from app.config import app, db
from controllers.authentication import auth_api
from database.models import User


class AuthTestCase(unittest.TestCase):

    def setUp(self):
        app.config.update({
            "TESTING": True,
            "TEMP_DB": True,
            "WTF_CSRF_ENABLED": False,
            "DEBUG": False
        })
        self.app = app.test_client()
        self.assertEqual(app.debug, False)
        db.disconnect()
        db.connect('sample_test')
        User.drop_collection()
        app.register_blueprint(auth_api, url_prefix='/api/auth')

    def test_loginFailed(self):
        response = self.app.post('/api/auth/login',
                                 data=json.dumps(dict(username='admin', password='password')),
                                 content_type='application/json',
                                 follow_redirects=True)
        self.assertEqual(401, response.status_code)

    def test_loginSuccess(self):
        user = User(username="admin", password="admin", role="SUPPORTER")
        user.hash_password()
        user.save()
        response = self.app.post('/api/auth/login',
                                 data=json.dumps(dict(username='admin', password='admin')),
                                 content_type='application/json',
                                 follow_redirects=True)
        self.assertEqual(200, response.status_code)

    def test_loginSuccessWithUPPERCaseUsername(self):
        user = User(username="admin", password="admin", role="SUPPORTER")
        user.hash_password()
        user.save()
        response = self.app.post('/api/auth/login',
                                 data=json.dumps(dict(username='ADMIN', password='admin')),
                                 content_type='application/json',
                                 follow_redirects=True)
        self.assertEqual(200, response.status_code)

    def test_cannotLoginWithBlankPasswordOrBlankUsername(self):
        user = User(username="supporter", password="supporter", role="SUPPORTER")
        user.hash_password()
        user.save()

        response = self.app.post('/api/auth/login',
                                 data=json.dumps(dict(username='', password='supporter')),
                                 content_type='application/json',
                                 follow_redirects=True)
        self.assertEqual(401, response.status_code)
        self.assertIn('Username can not be blank', response.json.get('message', None))

        response = self.app.post('/api/auth/login',
                                 data=json.dumps(dict(username='abc', password='')),
                                 content_type='application/json',
                                 follow_redirects=True)
        self.assertEqual(401, response.status_code)
        self.assertIn('Password can not be blank', response.json.get('message', None))
