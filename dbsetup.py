from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
# dir = os.path.dirname(__file__)
# databasefile = os.path.join(dir, 'CashMeAppData.db')

db_path = os.path.join(os.path.dirname(__file__), 'CashMeAppData.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)
