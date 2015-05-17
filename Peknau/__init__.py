__author__ = 'gareth'
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
# Main app settings
app = Flask(__name__)
db = SQLAlchemy(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = '\xf9\x19\x96_\xcf\xc1\x97i\xfc\xb3\x85\xd1n4n!\x0e3\x08\xb7\xb86\x19g'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'Peknau.db')
db.text_factory = str
# Import Modules
import view
import model
