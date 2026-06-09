from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

db = SQLAlchemy(app)

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), unique=True, nullable=False)

    password = db.Column(db.String(120), nullable=False)

@app.route("/")
def home():
    return render_template("index.html")

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        print(f"Username: {username}")
        print(f"Password: {password}")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        print(f"Register Username: {username}")
        print(f"Register Password: {password}")
        print(f"Confirm Password: {confirm_password}")

    return render_template("register.html")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)