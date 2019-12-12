import base64
from datetime import datetime, timedelta
from hashlib import md5
import os
import pandas as pd
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from app.search import add_to_index, remove_from_index, query_index
from sklearn.preprocessing import MultiLabelBinarizer

GENRES = ['action', 'adventure', 'art', 'autobiography', 'anthology', 'biography', "childrens", 'cookbook',
          'comic', 'diary', 'dictionary', 'crime', 'encyclopedia', 'drama', 'guide', 'fairytale', 'health',
          'fantasy', 'history', 'graphic', 'journal', 'historical', 'math', 'horror', 'memoir', 'mystery', 'prayer',
          'paranormal', 'religion', 'picture', 'textbook', 'poetry', 'review', 'political', 'crime', 'science',
          'romance', 'satire', 'travel', 'scifi', 'short', 'suspense', 'thriller', 'ya', 'modern', 'classic',
          'detective', 'war', 'period']

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

    def __repr__(self):

        return '<User {}>'.format(self.username)

    def get_ratings(self):

        ratings = self.ratings.join(Book).add_columns(Book.title, Book.genres).all()

        return list(sorted(map(lambda x: {"title": x[1], "rating": x[0].value, "genres": x[2].replace("|", ", ")}, ratings),
                           key=lambda x: x["rating"], reverse=True))

    def get_recommendations(self):

        books = pd.DataFrame([book.to_dict() for book in Book.query.all()])

        books = books.rename({"id": "book_id"}, axis=1)
        books = books.set_index("book_id")

        books["genres"] = books.genres.str.split("|")

        mlb = MultiLabelBinarizer()

        books_with_genres = books.join(pd.DataFrame(mlb.fit_transform(books.pop("genres")), columns=mlb.classes_,index=books.index))

        books_with_genres = books_with_genres.drop("title", axis=1)

        ratings = pd.DataFrame([rating.to_dict() for rating in self.ratings.all()])

        if not ratings.empty:

            ratings = ratings.rename({"value": "rating"}, axis=1)
            ratings = ratings.drop(["id", "user_id"], axis=1)
            ratings = ratings.set_index("book_id")
            ratings = ratings.sort_index()

            merged = pd.merge(books_with_genres, ratings, on="book_id")

            user_genres = merged.drop("rating", axis=1)
            user_ratings = ratings

            profile = user_genres.T.dot(user_ratings.rating)

            recommendations = (books_with_genres.dot(profile)) / profile.sum()
            recommendations = recommendations.sort_values(ascending=False)
            recommendations = recommendations.rename("recommendation", axis=1)

            data = pd.merge(books, recommendations, on="book_id")

            data.drop(user_ratings.index, inplace=True)  # Remove books already rated by the user.

            actual = data.to_dict("records")[:10]

            return actual

        return books[:10].to_dict("records")

    def set_password(self, password):

        self.password_hash = generate_password_hash(password)

    def check_password(self, password):

        return check_password_hash(self.password_hash, password)

    def avatar(self, size):

        digest = md5(self.email.lower().encode('utf-8')).hexdigest()

        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

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

class Rating(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    value = db.Column(db.Integer)

    def __repr__(self):

        return '<Rating {} {} {}>'.format(self.user_id, self.book_id, self.value)

class Book(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    genres = db.Column(db.String(200))

    def __repr__(self):

        return '<Book {}>'.format(self.title)