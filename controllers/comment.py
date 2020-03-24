from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine import errors
from database.models import Ticket, Comment
from helper.time import current_milli_time

comment_api = Blueprint('comment_api', __name__)


@comment_api.route("/<ticket_id>", methods=['POST'])
@jwt_required
def create_comment(ticket_id):
    error = validate_ticket(ticket_id)
    if error is not None:
        return error
    body = request.get_json()
    if body is None:
        return jsonify({'message': "content can not empty"}), 400
    content = body.get('content', None)
    if content is None:
        return jsonify({'message': "content can not empty"}), 400
    user_id = get_jwt_identity()
    comment = Comment(userId=user_id, content=content, createTime=current_milli_time(), ticketId=ticket_id) \
        .save()

    return jsonify(comment), 200


@comment_api.route("/view/<ticket_id>", methods=['POST'])
@jwt_required
def get_comment(ticket_id):
    try:
        error = validate_ticket(ticket_id)
        if error is not None:
            return error
        body = request.get_json()
        page_size = 10
        page = 1
        if body is not None:
            page_size = body.get('pageSize', page_size)
            page = body.get('page', page)
        comments = Comment.objects.order_by('-createTime').filter(ticketId=ticket_id).paginate(page=page, per_page=page_size)
    except errors.ValidationError:
        return jsonify({'message': 'error validate'}), 400

    return jsonify({'data': comments.items, 'has_next': comments.has_next, \
                    'has_prev': comments.has_prev, 'next_num': comments.next_num, \
                    'pages': comments.pages, 'page': comments.page, 'total': comments.total}), 200


@comment_api.route("/<comment_id>", methods=['DELETE'])
@jwt_required
def delete_my_comment(comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
    except errors.ValidationError:
        return jsonify({'message': 'Invalid comment Id'}), 400
    except errors.DoesNotExist:
        return jsonify({'message': 'Comment not found'}), 400
    user_id = get_jwt_identity()
    if comment.userId is not user_id:
        return jsonify({'message': 'You can not delete other comment !'}), 403

    comment.delete()
    return jsonify({'ok': True}), 200


def validate_ticket(ticket_id):
    error = None
    try:
        Ticket.objects.get(id=ticket_id)
    except errors.ValidationError:
        error = jsonify({'message': 'Invalid Ticket Id'}), 400
    except errors.DoesNotExist:
        error = jsonify({'message': 'Not found Ticket'}), 400

    return error
