
##TODAY IS JUNE 12, 2026 AT 1:05 PM EST
##THIS WAS FINALLY MIGRATED NEON POSTGRESQL
##TODAY IS JUNE 14, 2026 AT 8:09 PM EST
##GOOGLE OAUTH IS FINALLY WORKING BUT JUST LOCALLY
##ONE STEP CLOSER THAT I CAN TASTE IT
##HAHAHAHAHA HELL YEAH

import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, flash
from authlib.integrations.flask_client import OAuth
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from models import db, User, Post, Comment, AuditLog

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,
    "pool_recycle": 300
}

db.init_app(app)

oauth = OAuth(app)

google = oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile"
    }
)

@app.route("/login/google")
def google_login():
    redirect_uri = url_for("google_authorized", _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route("/login/google/authorized")
def google_authorized():
    token = google.authorize_access_token()
    user_info = token["userinfo"]

    email = user_info["email"]
    username = user_info.get("name", email.split("@")[0])

    user = User.query.filter_by(email=email).first()

    if not user:
        user = User(
            username=username,
            email=email,
            password="GOOGLE_OAUTH_USER",
            auth_provider="google"
        )

        db.session.add(user)
        db.session.commit()

    session["username"] = user.username
    
    log_event("GOOGLE_LOGIN_SUCCESS", user.username)

    flash("Logged in with Google.")

    return redirect(url_for("dashboard"))


def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if "username" not in session:
            return redirect(url_for("login"))

        return f(*args, **kwargs)

    return decorated_function


def log_event(action, username=None):
    log = AuditLog(
        username=username,
        action=action,
        ip_address=request.remote_addr
    )

    db.session.add(log)
    db.session.commit()


@app.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():

    user = User.query.filter_by(
        username=session["username"]
    ).first()

    if request.method == "POST":

        bio = request.form.get("bio")

        user.bio = bio

        db.session.commit()

        flash("Profile updated.")

        return redirect(url_for("profile"))

    return render_template(
        "edit_profile.html",
        user=user
    )


@app.route("/")
def home():
    return render_template("index.html")


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))

        user = User.query.filter_by(username=session["username"]).first()

        if not user or not user.is_admin:
            flash("Admin access required.")
            log_event("ADMIN_ACCESS_DENIED", session.get("username"))
            return redirect(url_for("dashboard"))

        return f(*args, **kwargs)

    return decorated_function


@app.route("/admin")
@login_required
@admin_required
def admin_dashboard():
    users = User.query.all()
    log_event("ADMIN_ACCESS_GRANTED", session.get("username"))
    return render_template("admin.html", users=users)


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
            
            log_event("LOGIN_SUCCESS", user.username)

            return redirect(url_for("dashboard"))

        else:
            
            log_event("LOGIN_FAILURE", username)

            flash("Invalid username or password.")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():

    return render_template(
        "dashboard.html",
        username=session["username"]
    )


@app.route("/posts", methods=["GET", "POST"])
@login_required
def posts():
    user = User.query.filter_by(username=session["username"]).first()

    if request.method == "POST":
        content = request.form.get("content")

        new_post = Post(content=content, user_id=user.id)

        db.session.add(new_post)
        db.session.commit()

        flash("Post created.")

        return redirect(url_for("posts"))

    page = request.args.get("page", 1, type=int)

    search_query = request.args.get("q")

    if search_query:
        posts = Post.query.filter(
            Post.content.contains(search_query)
        ).order_by(
            Post.created_at.desc()
        ).paginate(
            page=page,
            per_page=5
        )
    else:
        posts = Post.query.order_by(
            Post.created_at.desc()
        ).paginate(
            page=page,
            per_page=5
        )

    return render_template("posts.html", posts=posts)


@app.route("/add-comment/<int:post_id>", methods=["POST"])
@login_required
def add_comment(post_id):
    user = User.query.filter_by(username=session["username"]).first()

    post = Post.query.get_or_404(post_id)

    content = request.form.get("content")

    new_comment = Comment(
        content=content,
        user_id=user.id,
        post_id=post.id
    )

    db.session.add(new_comment)
    db.session.commit()

    flash("Comment added.")

    return redirect(url_for("posts"))


@app.route("/edit-comment/<int:comment_id>", methods=["GET", "POST"])
@login_required
def edit_comment(comment_id):
    user = User.query.filter_by(username=session["username"]).first()

    comment = Comment.query.get_or_404(comment_id)

    if comment.user_id != user.id:
        flash("You are not allowed to edit this comment.")
        return redirect(url_for("posts"))

    if request.method == "POST":
        comment.content = request.form.get("content")

        db.session.commit()

        flash("Comment updated.")

        return redirect(url_for("posts"))

    return render_template("edit_comment.html", comment=comment)


@app.route("/delete-post/<int:post_id>", methods=["POST"])
@login_required
def delete_post(post_id):
    user = User.query.filter_by(username=session["username"]).first()

    post = Post.query.get_or_404(post_id)

    if post.user_id != user.id:
        flash("You are not allowed to delete this post.")
        return redirect(url_for("posts"))

    db.session.delete(post)
    db.session.commit()

    flash("Post deleted.")

    return redirect(url_for("posts"))


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@login_required
def edit_post(post_id):

    user = User.query.filter_by(
        username=session["username"]
    ).first()

    post = Post.query.get_or_404(post_id)

    if post.user_id != user.id:
        flash("You are not allowed to edit this post.")
        return redirect(url_for("posts"))

    if request.method == "POST":

        post.content = request.form.get("content")

        db.session.commit()

        flash("Post updated.")

        return redirect(url_for("posts"))

    return render_template(
        "edit_post.html",
        post=post
    )


@app.route("/profile")
@login_required
def profile():

    user = User.query.filter_by(username=session["username"]).first()

    return render_template("profile.html", user=user)


@app.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():

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
@login_required
def delete_account():

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


@app.route("/delete-comment/<int:comment_id>", methods=["POST"])
@login_required
def delete_comment(comment_id):
    user = User.query.filter_by(username=session["username"]).first()

    comment = Comment.query.get_or_404(comment_id)

    if comment.user_id != user.id:
        flash("You are not allowed to delete this comment.")
        return redirect(url_for("posts"))

    db.session.delete(comment)
    db.session.commit()

    flash("Comment deleted.")

    return redirect(url_for("posts"))


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
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        existing_user = User.query.filter_by(username=username).first()

        existing_email = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Username already exists.")
            return redirect(url_for("register"))
        
        if existing_email:
            flash("Email already exists.")
            return redirect(url_for("register"))

        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
            auth_provider="local"
        )
        
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully. Please log in.")
        return redirect(url_for("login"))

    return render_template("register.html")


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)