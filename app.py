from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import bcrypt

# from datetime import datetime
# from flask_login import UserMixin

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///noobauth.db"
app.secret_key = "something"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# app.app_context()
# app.config['SECRET_KEY'] = 'something'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String())

    def __init__(self, email, password, name):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        # self.password=password

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))
        # return password


with app.app_context():
    db.create_all()

# **************************************----------- Home page ----************************************


@app.route("/")
def hello():
    return render_template("index.html")



# **************************************----------- Login ----************************************
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            # session["name"]=user.name
            session["email"] = user.email
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid User Ho tum")

    # return "Hello Flask with python"
    return render_template("login.html")

# **************************************----------- Register ----************************************
@app.route("/register", methods=["GET", "POST"])
def register():
    # return "Hello Flask with python"
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        new_user = User(email=email, password=password, name=name)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/login")

    return render_template("register.html")


# **************************************----------- Dashboard ----************************************
@app.route("/dashboard")
def dashboard():
    if session["email"]:
        user = User.query.filter_by(email=session["email"]).first()
        return render_template("dashboard.html", user=user)
    return redirect("/login")


# **************************************----------- Logout ----************************************
@app.route("/logout")
def logout():
    session.pop("email", None)  # remove username from the session if
    return redirect('/')




if __name__ == "__main__":
    app.run(debug=True, port=9000)
