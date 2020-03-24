import json
import unittest

from app.config import app, db
from controllers.authentication import auth_api
from controllers.users import user_api
from database.models import User
from helper import testUtil


class UserTestCase(unittest.TestCase):

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
        app.register_blueprint(user_api, url_prefix='/api/user')
        self.supporter = User(username="supporter", password="supporter", role="SUPPORTER")
        self.supporter.hash_password()
        self.supporter.save()
        self.user = User(username="user", password="user", role="USER")
        self.user.hash_password()
        self.user.save()

    def test_supporterCanCreateUser(self):
        testUtil.test_help_login(self.app, self.supporter.username, self.supporter.username)
        response = self.app.post('/api/user/create',
                                 data=json.dumps(dict(username='user1', password='user1', role='USER')),
                                 content_type='application/json',
                                 follow_redirects=True)
        self.assertEqual(200, response.status_code)

    def test_userShouldNotAbleToCreateNewUser(self):
        testUtil.test_help_login(self.app, self.user.username, self.user.username)
        response = self.app.post('/api/user/create',
                                 data=json.dumps(dict(username='user1', password='user1', role='USER')),
                                 content_type='application/json',
                                 follow_redirects=True)
        self.assertEqual(403, response.status_code)

    def test_userCanViewOtherUserProfile(self):
        testUtil.test_help_login(self.app, self.user.username, self.user.username)
        response = self.app.get('/api/user/all',
                                content_type='application/json',
                                follow_redirects=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.json))
