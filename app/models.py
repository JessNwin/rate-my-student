
from app import db 
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True) #Username
    full_name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.LargeBinary)