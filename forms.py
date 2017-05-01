from flask_wtf import Form
from wtforms import StringField,PasswordField,SubmitField,FloatField
from wtforms.validators import DataRequired,Email,Length

class SignupForm(Form):
    first_name = StringField("First Name",validators=[DataRequired("Please Enter Your First Name.")])
    last_name = StringField("Last Name",validators=[DataRequired("Please Enter Your Last Name.")])
    email = StringField("Email",validators=[DataRequired("Please Enter A Valid Email Address.\nexample@gmail.com")                                                                          ,Email("Invalid Email")])
    user_name = StringField("User Name",validators=[DataRequired("Please Enter A Desired Username.")])
    password = PasswordField("Password",validators=[DataRequired("Enter a password"),Length(min = 6)])
    submit = SubmitField("Sign Up")

class LoginForm(Form):
    email = StringField('Email',validators=[DataRequired("Please Enter Your Email"),Email("Invalid Email")])
    password = PasswordField("Password", validators=[DataRequired("Enter Your password")])
    submit = SubmitField("Sign in")

class AddFriend(Form):
    username = StringField('Add Friend',validators=[DataRequired("Please Enter A User You Would Like to Add")])

class PaymentForm(Form):
    paymentAmount = FloatField("Payment Amount",validators=[DataRequired("Enter Amount")])

class SelectFriendForm(Form):
    friendToPay = StringField("Select Friend",validators=[DataRequired("Select A Friend To Pay")])



