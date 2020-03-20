import unittest

from flask import json

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
        app.register_blueprint(auth_api, url_prefix='/auth')

    def test_loginFailed(self):
        response = self.app.post('/auth/login',
                                 data=json.dumps(dict(username='admin', password='password')),
                                 content_type='application/json',
                                 follow_redirects=True)
        self.assertEqual(response.status_code, 401)

    def test_loginSuccess(self):
        user = User(username="admin", password="admin", role="ADMIN")
        user.hash_password()
        user.save()
        response = self.app.post('/auth/login',
                                 data=json.dumps(dict(username='admin', password='admin')),
                                 content_type='application/json',
                                 follow_redirects=True)
        self.assertEqual(response.status_code, 200)
