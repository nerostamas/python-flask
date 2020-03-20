from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine import NotUniqueError, errors

from database.models import Ticket
from helper.timeUtils import current_milli_time

ticket_api = Blueprint('ticket_api', __name__)


@ticket_api.route("/create", methods=['POST'])
@jwt_required
def create_ticket():
    data = request.get_json()
    title = data.get('title', None)
    content = data.get('content', None)
    if title is not None \
            and content is not None:
        try:
            user_id = get_jwt_identity()
            ticket = {
                'title': title,
                'createdBy': user_id,
                'content': content,
                'createTime': current_milli_time()
            }
            Ticket(**ticket).save()
        except NotUniqueError:
            return jsonify({"ok": False, "message": "Ticket exist"}), 400
        return jsonify({'ok': True, 'message': 'Ticket created successfully!'}), 200
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400


@ticket_api.route("/all", methods=['GET'])
@jwt_required
def get_all_ticket():
    tickets = Ticket.objects()
    return jsonify(tickets)


@ticket_api.route("/findMyTicket", methods=["GET"])
@jwt_required
def find_my_ticlet():
    user_id = get_jwt_identity()
    tickets = Ticket.objects().filter(createdBy=user_id)

    return jsonify(tickets)
