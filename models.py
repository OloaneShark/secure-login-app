
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), unique=True, nullable=False)

    password = db.Column(db.String(120), nullable=False)

    bio = db.Column(db.String(500), nullable=True)
    

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    content = db.Column(db.String(500), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    user = db.relationship("User", backref="posts")
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    content = db.Column(db.String(500), nullable=False)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    post_id = db.Column(
        db.Integer,
        db.ForeignKey("post.id"),
        nullable=False
    )

    user = db.relationship("User")
    post = db.relationship("Post", backref="comments")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)