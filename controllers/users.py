from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from mongoengine import NotUniqueError, ValidationError, DoesNotExist

from database.models import User, ROLE

user_api = Blueprint('user_api', __name__)


@user_api.route("/create", methods=['POST'])
@jwt_required
def create_user():
    data = request.get_json()
    username = data.get('username', None)
    password = data.get('password', None)
    role = data.get('role', None)
    if username is not None \
            and password is not None \
            and role is not None:
        try:
            if role not in ROLE:
                return jsonify({'message': 'invalid role'})

            user = User(**data)
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


@user_api.route("/update/<id>", methods=['PUT'])
@jwt_required
def update_user(id):
    body = request.get_json()
    try:
        User.objects.get(id=id).update(**body)
    except ValidationError:
        return jsonify({'message': 'Invalid data'}), 400
    except DoesNotExist:
        return jsonify({'message': 'Not found data'}), 400
    except NotUniqueError:
        return jsonify({'message': "username existed"}), 400
    return '', 200
