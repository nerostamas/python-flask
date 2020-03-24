from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine

app = Flask(__name__, static_folder='fe/')
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_PATH'] = '/api/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/auth/refresh'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['SECRET_KEY'] = 'hello-python-after-2-years'
app.config['MONGODB_SETTINGS'] = {
    'db': 'sample',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
