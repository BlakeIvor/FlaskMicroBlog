from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin,db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True, index=True)
    
    email: so.Mapped[str] = so.mapped_column(sa.String(120), unique=True)
    
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(128))
    
    posts: so.WriteOnlyMapped['Post'] = so.relationship('Post', back_populates='author')
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(sa.DateTime, index=True, default=datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('user.id'), index=True)
    
    author: so.Mapped[User] = so.relationship('User', back_populates='posts')

    def __repr__(self):
        return '<Post {}>'.format(self.body)


# The user_loader callback will be registered in __init__.py
def load_user(id):
    return User.query.get(int(id))