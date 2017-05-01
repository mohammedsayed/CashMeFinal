from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from dbsetup import db



class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(80), unique=True,primary_key=True)
    firstName = db.Column(db.String(80),unique=False)
    lastName = db.Column(db.String(80),unique=False)
    balance = db.Column(db.FLOAT,unique=False)
    email = db.Column(db.String(20),unique=True)
    creditcardno = db.Column(db.String(16),unique=True)
    passwordhash = db.Column(db.String(50))




    def __init__(self,firstName,lastName,email,username,password):
        self.username = username
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.balance = 0.00
        self.set_password(password)



    def __repr__(self):
        return '<User %r>' % self.username

    def set_password(self,pword):
        self.passwordhash = generate_password_hash(pword)

    def set_credit_card(self,cc):
        self.creditcardno = cc

    def check_password(self,pword):
        return check_password_hash(self.passwordhash,pword)


class Friendship(db.Model):
    __tablename__ = 'friendships'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String(80), unique=False,primary_key=False)
    friendUserName = db.Column(db.String(80), unique=False,primary_key=False)

    def __init__(self,username,friendUser):
        self.username = username
        self.friendUserName = friendUser



