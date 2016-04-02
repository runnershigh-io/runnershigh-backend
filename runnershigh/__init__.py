import os
import sys
import config

from flask import Flask, render_template
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt

server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI
server.config['SECRET_KEY'] = config.SECRET_KEY
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(server)
bcrypt = Bcrypt(server)

login_manager = LoginManager()
login_manager.init_app(server)

from revolvr.auth.views import mod as AuthModule
server.register_blueprint(AuthModule)

from revolvr.path.views import mod as PathModule
server.register_blueprint(PathModule)

from revolvr.user.views import mod as UserModule
server.register_blueprint(UserModule)
