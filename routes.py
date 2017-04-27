from flask import Flask, render_template,request,session,redirect,url_for
from models import User,db,Friendship
from forms import SignupForm,LoginForm,AddFriend
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
  return render_template("search.html")

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
        return redirect(url_for("success"))
      else:
        return redirect(url_for("addfriend"))
  elif request.method == "GET":
    return render_template("addfriend.html", form=form)









if __name__ == "__main__":
  app.run(debug=True)

