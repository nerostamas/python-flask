import json
import unittest

from app.config import app, db
from controllers.authentication import auth_api
from controllers.comment import comment_api
from controllers.ticket import ticket_api
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
        app.register_blueprint(ticket_api, url_prefix='/api/ticket')
        app.register_blueprint(comment_api, url_prefix='/api/comment')
        self.supporter = User(username="supporter", password="supporter", role="SUPPORTER")
        self.supporter.hash_password()
        self.supporter.save()
        self.user = User(username="user", password="user", role="USER")
        self.user.hash_password()
        self.user.save()

    def test_userCanCreateTicket(self):
        testUtil.test_help_login(self.app, self.user.username, self.user.username)
        response = self.app.post('/api/ticket/create',
                                 data=json.dumps(dict(title='Ticket1', content='this is my content')),
                                 content_type='application/json',
                                 follow_redirects=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('this is my content', response.json.get('content'))

    def test_supporterCanNotCreateTicket(self):
        testUtil.test_help_login(self.app, self.supporter.username, self.supporter.username)
        response = self.app.post('/api/ticket/create',
                                 data=json.dumps(dict(title='Ticket1', content='this is my content')),
                                 content_type='application/json',
                                 follow_redirects=True)
        self.assertEqual(403, response.status_code)

    def test_supporterAndUserCanReplyTicket(self):
        testUtil.test_help_login(self.app, self.user.username, self.user.username)
        response = self.app.post('/api/ticket/create',
                                 data=json.dumps(dict(title='Ticket1', content='this is my content')),
                                 content_type='application/json',
                                 follow_redirects=True)
        self.assertEqual(200, response.status_code)
        ticket_id = response.json.get('_id').get('$oid')
        response = self.app.post('/api/comment/' + str(ticket_id),
                                 data=json.dumps(dict(content='this is comment from user')),
                                 content_type='application/json',
                                 follow_redirects=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('this is comment from user', response.json.get('content'))

        # switch to supporter
        testUtil.test_help_login(self.app, self.supporter.username, self.supporter.username)
        response = self.app.post('/api/comment/' + str(ticket_id),
                                 data=json.dumps(dict(content='this is comment from supporter')),
                                 content_type='application/json',
                                 follow_redirects=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('this is comment from supporter', response.json.get('content'))

    def test_canNotDeleteOthersComment(self):
        testUtil.test_help_login(self.app, self.user.username, self.user.username)
        response = self.app.post('/api/ticket/create',
                                 data=json.dumps(dict(title='Ticket1', content='this is my content')),
                                 content_type='application/json',
                                 follow_redirects=True)
        self.assertEqual(200, response.status_code)
        ticket_id = response.json.get('_id').get('$oid')
        response = self.app.post('/api/comment/' + str(ticket_id),
                                 data=json.dumps(dict(content='this is comment from user')),
                                 content_type='application/json',
                                 follow_redirects=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('this is comment from user', response.json.get('content'))
        user_comment_id = response.json.get('_id').get('$oid')

        # switch to supporter
        testUtil.test_help_login(self.app, self.supporter.username, self.supporter.username)
        response = self.app.post('/api/comment/' + str(ticket_id),
                                 data=json.dumps(dict(content='this is comment from supporter')),
                                 content_type='application/json',
                                 follow_redirects=True)
        self.assertEqual(200, response.status_code)
        sp_comment_id = response.json.get('_id').get('$oid')
        self.assertEqual('this is comment from supporter', response.json.get('content'))

        # supporter can not delete user's reply
        response = self.app.delete('/api/comment/' + str(user_comment_id),
                                   content_type='application/json',
                                   follow_redirects=True)
        self.assertEqual(403, response.status_code)

        # user can not delete sp's reply
        # switch back to user
        testUtil.test_help_login(self.app, self.user.username, self.user.username)
        response = self.app.delete('/api/comment/' + str(sp_comment_id),
                                   content_type='application/json',
                                   follow_redirects=True)
        self.assertEqual(403, response.status_code)
