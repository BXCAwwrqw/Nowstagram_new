#-*- encoding=UTF-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app= Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.config.from_pyfile('app.conf')
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='/reglogin'
app.secret_key='some secret'

from Nowstagram import view,models