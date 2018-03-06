# -*- encoding=UTF-8 -*-
from Nowstagram import db, login_manager
import random
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(32))
    head_url = db.Column(db.String(256))
    salt = db.Column(db.String(32))
    images = db.relationship('Image', backref='user', lazy='dynamic')

    def __init__(self, username, password, salt=''):
        self.username = username
        self.password = password
        self.salt = salt
        self.head_url = 'https://www.gravatar.com/avatar/fc35e0f354c03' + str(random.randint(0, 1000)) + '0cf6db5b65c86ef5905c?s=328&d=identicon&r=PG&f=1'

    def __repr__(self):
        return '<User %d %s>' % (self.id, self.username)

    @login_manager.user_loader # 管理此类
    def load_user(user_id):
        return User.query.get(user_id)

    @property
    def is_authenticated(self):
        print 'is_authenticated'
        return True

    @property
    def is_active(self):
        print 'is_active'
        return True

    @property
    def is_anonymous(self):
        print 'is_anonymous'
        return False

    def get_id(self):
        print 'get_id'
        return self.id


class Comment(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(1024))
    imag_id = db.Column(db.Integer, db.ForeignKey('image.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.Integer, default=0)
    user = db.relationship('User')

    def __init__(self, content, user_id, imag_id):
        self.content = content
        self.user_id = user_id
        self.imag_id = imag_id

    def __repr__(self):
        return '<Comment %d %s>' % (self.id, self.content)


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(512))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_time = db.Column(db.DateTime)
    comments = db.relationship('Comment')

    def __init__(self, url, user_id):
        self.url = url
        self.user_id = user_id
        self.created_time = datetime.now()

    def __repr__(self):
        return '<Image %d %s>' % (self.id, self.url)


