
__author__ = 'gareth'
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CsrfProtect
import os


# Main app settings
app = Flask(__name__)
app.debug = True
#security
csrf = CsrfProtect()
csrf.init_app(app)
# database
db = SQLAlchemy(app)
# login manager
login_manager = LoginManager()
login_manager.init_app(app)
# base app settings
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['WTF_CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = '\xf9\x19\x96_\xcf\xc1\x97i\xfc\xb3\x85\xd1n4n!\x0e3\x08\xb7\xb86\x19g'
app.config['WTF_CSRF_SECRET_KEY'] = app.config['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'Peknau.db')
db.text_factory = str

@app.template_filter('is_list')
def is_list(value):
    return isinstance(value, list)
app.jinja_env.filters['reverse'] = is_list


# Import Modules
import views
import models
import forms
