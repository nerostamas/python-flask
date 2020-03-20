from flask_bcrypt import generate_password_hash, check_password_hash

from .mongodb import db

ROLE = ["ADMIN", "SUPPORTER", "USER"]


class User(db.Document):
    username = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
    role = db.StringField(required=True)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Ticket(db.Document):
    title = db.StringField(required=True)
    createdBy = db.StringField(required=True)
    content = db.StringField(required=True)
    createTime = db.IntField(required=True)


class Comment(db.Document):
    userId = db.StringField(required=True)
    ticketId = db.StringField(required=True)
    content = db.StringField(required=True)
    createTime = db.IntField(required=True)
