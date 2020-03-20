from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine import errors

from helper.timeUtils import current_milli_time

from database.models import Ticket, Comment

comment_api = Blueprint('comment_api', __name__)


@comment_api.route("/<ticket_id>", methods=['POST'])
@jwt_required
def create_comment(ticket_id):
    validate_ticket(ticket_id)
    body = request.get_json()
    if body is None:
        return jsonify({'message': "content can not empty"}), 400
    user_id = get_jwt_identity()
    content = body.get('content', None)
    if content is None:
        return jsonify({'message': "content can not empty"}), 400
    comment = Comment(userId=user_id, content=content, createTime=current_milli_time(), ticketId=ticket_id) \
        .save()

    return jsonify(comment), 200


@comment_api.route("/<ticket_id>", methods=['GET'])
@jwt_required
def get_comment(ticket_id):
    validate_ticket(ticket_id)
    try:
        comment = Comment.objects.filter(ticketId=ticket_id)
    except errors.ValidationError:
        return jsonify({'message': 'error validate'}), 400

    return jsonify(comment), 200


@comment_api.route("/<comment_id>", methods=['DELETE'])
@jwt_required
def delete_my_comment(comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
    except errors.ValidationError:
        return jsonify({'message': 'Invalid comment Id'}), 400
    except errors.DoesNotExist:
        return jsonify({'message': 'Comment not found'}), 400

    comment.delete()
    return jsonify({'ok': True}), 200


def validate_ticket(ticket_id):
    try:
        Ticket.objects.get(id=ticket_id)
    except errors.ValidationError:
        return jsonify({'message': 'Invalid Ticket Id'}), 400
    except errors.DoesNotExist:
        return jsonify({'message': 'Not found Ticket'}), 400
