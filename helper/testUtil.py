import json


def test_help_login(app, username, password):
    app.post('/api/auth/login',
             data=json.dumps(dict(username=username, password=password)),
             content_type='application/json',
             follow_redirects=True)
