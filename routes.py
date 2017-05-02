from flask import Flask, render_template, request, session, redirect, url_for, flash
from models import User,db,Friendship
from forms import *
from dbsetup import app




app.secret_key = "development-key"


@app.route("/")
def index():
  return render_template("index.html")

@app.route("/about")
def about():
  return render_template("about.html")

@app.route("/signup",methods=["GET","POST"])
def signup():
  if "email" in session:
   return redirect(url_for("home"))
  form = SignupForm()

  if request.method == "POST":
    if form.validate() == False:
      return render_template("signup.html",form = form)
    else:
      newuser = User(form.first_name.data,form.last_name.data,form.email.data,form.user_name.data,form.password.data)
      db.session.add(newuser)
      db.session.commit()
      session["email"] = newuser.email
      session["username"] = newuser.username
      return redirect(url_for("home"))
  elif request.method == "GET":
    return render_template("signup.html",form = form)

@app.route("/home")
def home():
   if "email" not in session:
     return redirect(url_for("login"))

   return render_template("home.html")

@app.route("/login",methods=["GET","POST"])
def login():
  if "email" in session:
   return redirect(url_for("home"))
  form = LoginForm()
  if request.method == "POST":
    if form.validate() == False:
      return render_template("login.html",form = form)
    else:
      email = form.email.data
      password = form.password.data
      user = User.query.filter_by(email=email).first()
      print (user.email)
      if user is not None and user.check_password(password):
        session["email"] = form.email.data
        session["username"] = user.username
        return redirect(url_for("home"))
      else:
        return redirect(url_for("login"))
  elif request.method == "GET":
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
  session.pop('email',None)
  return redirect(url_for("index"))

@app.route("/search")
def search():
  if "email" not in session:
    return redirect(url_for("login"))
  else:
    friendslist1 = Friendship.query.filter_by(username=session["username"]).all()
    friendslist2 = Friendship.query.filter_by(friendUserName=session["username"])
    strFriendList = [""]
    for friend in friendslist1:
      strFriendList.append(friend.friendUserName)
    for friend in friendslist2:
      strFriendList.append(str(friend.username))
    form = SelectFriendForm()
    return render_template("search.html",strFriendList=strFriendList,form=form)



@app.route("/success")
def success():
  return render_template("success.html")

@app.route("/addfriend",methods=['GET', 'POST'])
def addfriend():
  if "email" not in session:
    return redirect(url_for("login"))
  form = AddFriend()
  if request.method == "POST":
    if form.validate() == False:
      return render_template("addfriend.html", form=form)
    else: ## add the user to the friendships list
      userNameToAdd = form.username.data
      usertoadd = User.query.filter_by(username=userNameToAdd).first()
      if usertoadd is not None:
        friendship = Friendship(session["username"],usertoadd.username)
        db.session.add(friendship)
        db.session.commit()
        return redirect(url_for("search"))
      else:
        return redirect(url_for("addfriend"))
  elif request.method == "GET":
    return render_template("addfriend.html", form=form)


@app.route("/payment", methods=['GET','POST'])
def payment():
    if "email" not in session:
        return redirect(url_for("login"))
    form = PaymentForm()
    if request.method == "POST":
        if form.validate() == False:
            session["userToPay"] = request.form.get('friendToPay')
            return render_template("payment.html", form=form)
        else:
            amount = form.paymentAmount.data
            friendToPay = User.query.filter_by(username=session["userToPay"]).first()
            currentUser = User.query.filter_by(email=session["email"]).first()
            if currentUser.balance >= float(amount):
                currentUser.balance = currentUser.balance - float(amount)
                friendToPay.balance = friendToPay.balance + float(amount)
                db.session.commit()
                flash("Payment Successful!")
            return render_template("payment.html", form=form)
    elif request.method == "GET":
        return render_template("payment.html", form=form)




@app.route("/balance")
def balance():
    if "email" not in session:
        return redirect(url_for("login"))
    currentUser =  currentUser = User.query.filter_by(email=session["email"]).first()
    userbal = currentUser.balance
    return render_template("balance.html",userbal=userbal,curUserName=currentUser.username)



if __name__ == "__main__":
  app.run(debug=True)

