from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, jwt_required

from auth.handleAuth import auth_api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_PATH'] = '/api/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/auth/refresh'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False

jwt = JWTManager(app)


app.register_blueprint(auth_api, url_prefix='/auth')


@app.route('/api/test')
@jwt_required
def get_response():
    return jsonify('You are an authenticate person to see this message')


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
