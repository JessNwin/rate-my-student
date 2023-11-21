
from flask import Flask
import os

app = Flask("Rate My Student")
# app.secret_key = os.environ['SECRET_KEY']
app.secret_key = 'OogaBooga'

# db initialization
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)

from app import models
with app.app_context(): 
    db.create_all()

# login manager
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

from app.models import User

# user_loader callback
@login_manager.user_loader
def load_user(id):
    try: 
        return db.session.query(User).filter(User.id==id).one()
    except: 
        return None
    
# cache setup in case we use cache
# from flask_caching import Cache
# cache = Cache()
# cache.init_app(app, config={
#     'CACHE_TYPE': 'simple',
#     'CACHE_DEFAULT_TIMEOUT': 300
# })

from app import routes