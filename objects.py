from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
import os
import datetime

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship


basedir = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
app.secret_key = "__jf*DJ*39h8FFF11234"

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

DATABASE_PATH = "database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{basedir}/{DATABASE_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    '''A model that represents a User'''

    __tablename__ = "user"

    id = Column(db.Integer, primary_key=True, autoincrement=True)
    notes = relationship("Note")
    login = Column(db.String)
    password = Column(db.String)


class Note(db.Model):
    '''A model that represents a Note'''

    __tablename__ = "note"

    id = Column(db.Integer, primary_key=True, autoincrement=True)
    author = Column(db.Integer, ForeignKey("user.id"))
    title = Column(db.String(100), nullable=True)
    text = Column(db.Text, nullable=False)
    created = Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    edited = Column(db.DateTime, nullable=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id==user_id).first()

# If there is no database file - create one with empty tables
if not os.path.exists(DATABASE_PATH):
    db.create_all()

if __name__ == "__main__":
    # Clear database if objects.py launched
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
        db.create_all()