import base64
from datetime import datetime, timedelta
from hashlib import md5
import os
from time import time
from flask import current_app, url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login
from app.search import add_to_index, remove_from_index, query_index


class SearchableMixin(object):

    @classmethod
    def search(cls, expression, page, per_page):

        ids, total = query_index(cls.__tablename__, expression, page, per_page)

        if total == 0:

            return cls.query.filter_by(id=0), 0

        when = []

        for i in range(len(ids)):

            when.append((ids[i], i))

        return cls.query.filter(cls.id.in_(ids)).order_by(db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):

        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):

        for obj in session._changes['add']:

            if isinstance(obj, SearchableMixin):

                add_to_index(obj.__tablename__, obj)

        for obj in session._changes['update']:

            if isinstance(obj, SearchableMixin):

                add_to_index(obj.__tablename__, obj)

        for obj in session._changes['delete']:

            if isinstance(obj, SearchableMixin):

                remove_from_index(obj.__tablename__, obj)

        session._changes = None

    @classmethod
    def reindex(cls):

        for obj in cls.query:

            add_to_index(cls.__tablename__, obj)


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    ratings = db.relationship("Rating", backref="rater", lazy="dynamic")

    # posts = db.relationship('Post', backref='author', lazy='dynamic')
    # about_me = db.Column(db.String(140))
    # last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    # token = db.Column(db.String(32), index=True, unique=True)
    # token_expiration = db.Column(db.DateTime)
    #
    # followed = db.relationship(
    #     'User', secondary=followers,
    #     primaryjoin=(followers.c.follower_id == id),
    #     secondaryjoin=(followers.c.followed_id == id),
    #     backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):

        return '<User {}>'.format(self.username)

    def get_ratings(self):

        ratings = self.ratings.join(Book).add_columns(Book.title).all()

        return list(map(lambda x: {"title": x[1], "rating": x[0].value}, ratings))

    def get_recommendations(self):

        # So the first one is my writing, right?
        # Yeah. Let's pre-generate it.

        """

        SELECT t2.movie
        FROM movies t1 INNER JOIN movies t2
             ON t1.user = 1
             AND t2.user IN(2,3,4,5,6,7)
             AND t2.movie NOT IN ( SELECT movie
                                   FROM movies
                                   WHERE user = 1 )
        GROUP BY(t2.movie)
        HAVING AVG(t2.rating)>=3
        AND  COUNT(DISTINCT t2.user) >= 3

        """

        recommendations = Book.join(Book, )

        # Lol. Far better to create this table ahead of time.
        # Cause it's going to be HUGE.

        # Of course, it's not quite that simple.
        # So let's get everything ship-shape here first.

        ratings = self.ratings.query(Book)




    def set_password(self, password):

        self.password_hash = generate_password_hash(password)

    def check_password(self, password):

        return check_password_hash(self.password_hash, password)

    def avatar(self, size):

        digest = md5(self.email.lower().encode('utf-8')).hexdigest()

        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def get_reset_password_token(self, expires_in=600):

        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):

        try:

            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']

        except:

            return

        return User.query.get(id)

    def to_dict(self):

        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash
        }

        return data

    def from_dict(self, data, new_user=False):

        for field in ['username', 'email', 'about_me']:

            if field in data:

                setattr(self, field, data[field])

        if new_user and 'password' in data:

            self.set_password(data['password'])

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user


@login.user_loader
def load_user(id):

    return User.query.get(int(id))


class Post(SearchableMixin, db.Model):

    __searchable__ = ['body']

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    language = db.Column(db.String(5))

    def __repr__(self):

        return '<Post {}>'.format(self.body)

class Rating(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    value = db.Column(db.Integer)

    def __repr__(self):

        return '<Rating {} {} {}>'.format(self.user_id, self.book_id, self.value)

    def to_dict(self):

        return {
            "id": self.id,
            "book_id": self.book_id,
            "user_id": self.user_id,
            "value": self.value
        }



class Book(db.Model):

    # __searchable__ = ['title']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    genres = db.Column(db.String(200))

    def __repr__(self):

        return '<Book {}>'.format(self.title)

    def to_dict(self):

        return {
            "id": self.id,
            "title": self.title,
            "genres": self.genres,
        }


class BookTag(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"))
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    count = db.Column(db.Integer)

    def __repr__(self):

        return '<BookTag {} {} {}>'.format(self.book_id, self.tag_id, self.count)

    def to_dict(self):

        return {
            "id": self.id,
            "book_id": self.book_id,
            "tag_id": self.tag_id,
            "count": self.count
        }

class Tag(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))

    def __repr__(self):

        return '<Book {}>'.format(self.name)

    def to_dict(self):

        return {
            "id": self.id,
            "name": self.name
        }

