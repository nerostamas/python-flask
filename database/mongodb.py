from app.config import db


def initialize_db(app):
    db.init_app(app)
