from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, \
    jwt_refresh_token_required, get_jwt_identity, unset_jwt_cookies

from flask import Blueprint

auth_api = Blueprint('auth_api', __name__)


@auth_api.route("/login", methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username != 'admin' or password != 'admin':
        return jsonify({'login': False}), 401

    # Create the tokens we will be sending back to the user
    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)

    # Set the JWT cookies in the response
    resp = jsonify({'login': True})
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
