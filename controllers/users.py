from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_claims, get_jwt_identity
from mongoengine import NotUniqueError, ValidationError, DoesNotExist

from database.models import User, ROLE

user_api = Blueprint('user_api', __name__)


@user_api.route("/my", methods=['GET'])
@jwt_required
def get_my_info():
    role = get_jwt_claims()['role']
    user_id = get_jwt_identity()
    try:
        user = User.objects.get(id=user_id)
    except ValidationError:
        return jsonify({'message': 'Invalid User Id'}), 400
    except DoesNotExist:
        return jsonify({'message': 'Not found user'}), 400

    return jsonify({'username': user.username, '_id': user_id, 'role': role}), 200


@user_api.route("/create", methods=['POST'])
@jwt_required
def create_user():
    role = get_jwt_claims()['role']
    if role not in ROLE or role == 'USER':
        return jsonify({'message': 'Permission denied'}), 403

    data = request.get_json()
    username = data.get('username', None)
    password = data.get('password', None)
    role = data.get('role', None)
    if username is not None \
            and password is not None \
            and role is not None:
        try:
            if len(username) < 3:
                return jsonify({'message': 'username must greater than 3 characters'}), 400
            nor_username = username.strip().lower()
            if nor_username.find(' ') != -1:
                return jsonify({'message': 'username should not have space'}), 400
            if role not in ROLE:
                return jsonify({'message': 'invalid role'}), 400

            user = User(username=nor_username, password=password, role=role)
            user.hash_password()
            user.save()

        except NotUniqueError:
            return jsonify({"ok": False, "message": "User exist"}), 400
        return jsonify({'ok': True, 'message': 'User created successfully!'}), 200
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400


@user_api.route("/all", methods=['GET'])
@jwt_required
def get_all_user():
    users = User.objects()
    return jsonify(users), 200


@user_api.route("/getByIds", methods=['POST'])
@jwt_required
def get_user_by_ids():
    body = request.get_json()
    if body is None:
        return jsonify({'message': 'Please provide ids'}), 400
    ids = body.get('ids', [])
    try:
        users = User.objects(id__in=ids)
    except ValidationError:
        return jsonify({'message': 'Invalid Ids'}), 400
    return jsonify(users), 200
