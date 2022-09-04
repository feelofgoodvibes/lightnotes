from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required
import os

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

basedir = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__)
app.secret_key = "__jf*DJ*39h8FFF11234"

# login_manager = LoginManager()
# login_manager.init_app(app)

DATABASE_PATH = "database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{basedir}/{DATABASE_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
