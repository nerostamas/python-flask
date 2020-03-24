from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims
from mongoengine import NotUniqueError, errors
from database.models import Ticket, ROLE
from helper.time import current_milli_time

ticket_api = Blueprint('ticket_api', __name__)


@ticket_api.route("/create", methods=['POST'])
@jwt_required
def create_ticket():
    role = get_jwt_claims()['role']
    if role not in ROLE or role != 'USER':
        return jsonify({'message': 'Only user can create ticket'}), 403

    data = request.get_json()
    title = data.get('title', None)
    content = data.get('content', None)
    if title is not None \
            and content is not None:
        try:
            user_id = get_jwt_identity()
            ticket_entity = {
                'title': title,
                'createdBy': user_id,
                'content': content,
                'createTime': current_milli_time()
            }
            ticket = Ticket(**ticket_entity).save()
        except NotUniqueError:
            return jsonify({"message": "Ticket exist"}), 400
        return jsonify(ticket), 200
    else:
        return jsonify({'message': 'Bad request parameters!'}), 400


@ticket_api.route("/all", methods=['GET'])
@jwt_required
def get_all_ticket():
    tickets = Ticket.objects()
    return jsonify(tickets)


@ticket_api.route("/byId/<id>", methods=['GET'])
def get_by_id(id):
    if id is None:
        return jsonify({'message': 'Invalid Id'}), 400
    try:
        ticket = Ticket.objects.get(id=id)
    except errors.ValidationError:
        return jsonify({'message': 'Validate error'}), 400
    except errors.DoesNotExist:
        return jsonify({'message': 'Ticket not found'}), 400

    return jsonify(ticket), 200


@ticket_api.route("/findMyTicket", methods=["GET"])
@jwt_required
def find_my_ticlet():
    user_id = get_jwt_identity()
    tickets = Ticket.objects().filter(createdBy=user_id)

    return jsonify(tickets)
