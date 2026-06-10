
from flask import Flask, render_template, request
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)

app.secret_key = "supersecretkey"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if "username" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):

            session["username"] = user.username

            return redirect(url_for("dashboard"))

        else:

            flash("Invalid username or password.")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "username" in session:
        return render_template("dashboard.html", username=session["username"])

    return redirect(url_for("login"))


@app.route("/profile")
def profile():

    if "username" not in session:
        return redirect(url_for("login"))

    user = User.query.filter_by(username=session["username"]).first()

    return render_template("profile.html", user=user)


@app.route("/change-password", methods=["GET", "POST"])
def change_password():

    if "username" not in session:
        return redirect(url_for("login"))

    user = User.query.filter_by(username=session["username"]).first()

    if request.method == "POST":

        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if not check_password_hash(user.password, current_password):

            flash("Current password is incorrect.")
            return redirect(url_for("change_password"))

        if new_password != confirm_password:

            flash("New passwords do not match.")
            return redirect(url_for("change_password"))

        hashed_password = generate_password_hash(new_password)

        user.password = hashed_password

        db.session.commit()

        flash("Password updated successfully.")

        return redirect(url_for("profile"))

    return render_template("change_password.html")


@app.route("/delete-account", methods=["GET", "POST"])
def delete_account():

    if "username" not in session:
        return redirect(url_for("login"))

    user = User.query.filter_by(username=session["username"]).first()

    if request.method == "POST":

        password = request.form.get("password")

        if not check_password_hash(user.password, password):

            flash("Incorrect password.")
            return redirect(url_for("delete_account"))

        db.session.delete(user)

        db.session.commit()

        session.pop("username", None)

        flash("Account deleted successfully.")

        return redirect(url_for("register"))

    return render_template("delete_account.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    
    if "username" in session:
        return redirect(url_for("dashboard"))
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash("Username already exists.")
            return redirect(url_for("register"))

        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        new_user = User(username=username, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully. Please log in.")
        return redirect(url_for("login"))

    return render_template("register.html")


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)