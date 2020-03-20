import datetime

from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, \
    jwt_refresh_token_required, get_jwt_identity, unset_jwt_cookies

from flask import Blueprint
from mongoengine import errors

from app.config import jwt
from database.models import User

auth_api = Blueprint('auth_api', __name__)


class JWTUser:
    def __init__(self, username, role):
        self.username = username
        self.role = role


@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {'role': user.role}


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.username


@auth_api.route("/login", methods=['POST'])
def login():
    body = request.get_json()
    if body is None:
        return jsonify({'message': 'Invalid username and password'}), 401

    username = body.get('username', None)
    password = body.get('password', None)

    # Create the tokens we will be sending back to the user
    try:
        user = User.objects.get(username=username)
    except errors.DoesNotExist:
        return jsonify({'message': 'username or password is not match'}), 401

    if user.check_password(password) is False:
        return jsonify({'message': 'username or password is not match'}), 401

    user = JWTUser(str(user.id), user.role)
    expires = datetime.timedelta(days=7)
    access_token = create_access_token(identity=user, expires_delta=expires)
    refresh_token = create_refresh_token(identity=user)

    # Set the JWT cookies in the response
    resp = jsonify({'login': 'Login success'})
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp, 200


@auth_api.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    # Create the new access token
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)

    # Set the JWT access cookie in the response
    resp = jsonify({'refresh': True})
    set_access_cookies(resp, access_token)
    return resp, 200


@auth_api.route('/logout', methods=['POST'])
def logout():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200
