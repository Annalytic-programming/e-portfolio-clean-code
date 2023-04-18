from uuid import uuid4

from flask_login import UserMixin

from clothesmanager import bcrypt
from clothesmanager import db


class User(db.Model, UserMixin):
    
    id = db.Column(db.Text, primary_key=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    
    def __repr__(self) -> str:
        return f'User("{self.username}")'
    
    @staticmethod
    def get_user_by_id(id):
        return User.query.filter_by(id=id).first()
    
    @staticmethod
    def get_user_by_username(username):
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def register_user(username, password):
        user = User(id=str(uuid4()), username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return True
    
    @staticmethod
    def login_user(username, password):
        user = User.query.filter_by(username=username).first()
        if user is None:
            return False
        return bool(bcrypt.check_password_hash(user.password, password))