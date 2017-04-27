from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///Users/mksmasr/PycharmProjects/CashMe_Master/CashMeAppData.db'
db = SQLAlchemy(app)
