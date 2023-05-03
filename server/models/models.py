from enum import Enum

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from sqlalchemy import func

from server import db, login_manager


class AccessCategories(Enum):
    first = 1
    second = 2
    third = 3


@login_manager.user_loader
def load_user(user):
    return User.query.get(int(user))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    access_category = db.Column(db.Enum(AccessCategories), default=AccessCategories.first, nullable=False)
    hidden_ads = db.relationship('Advertisements', secondary='hidden_ads',
                                 backref=db.backref('hidden_by', lazy='dynamic'))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password).decode('utf-8')


class Advertisements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    olx_id = db.Column(db.Integer, unique=True)
    url = db.Column(db.String(500))
    name = db.Column(db.String(64))
    price = db.Column(db.Integer)
    currency = db.Column(db.String(5))
    author_name = db.Column(db.String(64))
    image = db.Column(db.String(500))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<Advertisement {self.name}>'


hidden_ads = db.Table('hidden_ads',
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                      db.Column('ad_id', db.Integer, db.ForeignKey('advertisements.id'))
                      )
