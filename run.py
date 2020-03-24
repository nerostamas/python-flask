import os

from flask import send_from_directory

from app.config import app

# router
from controllers.authentication import auth_api
from controllers.ticket import ticket_api
from controllers.users import user_api
from controllers.comment import comment_api

# register router
app.register_blueprint(auth_api, url_prefix='/api/auth')
app.register_blueprint(user_api, url_prefix='/api/users')
app.register_blueprint(ticket_api, url_prefix='/api/ticket')
app.register_blueprint(comment_api, url_prefix='/api/comment')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run()
