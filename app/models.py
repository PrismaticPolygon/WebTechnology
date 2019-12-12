import base64
from datetime import datetime, timedelta
from hashlib import md5
import pandas as pd
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from scipy.sparse.linalg import svds
import numpy as np

def round_rating(number):

    return round(number * 2) / 2

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    ratings = db.relationship("Rating", backref="rater", lazy="dynamic")

    def __repr__(self):

        return '{}'.format(self.username)

    def get_ratings(self):

        ratings = self.ratings.join(Book).add_columns(Book.title, Book.genres, Book.id).all()

        ratings = [{
            "title": rating[1],
            "value": rating[0].value,
            "genres": rating[2].replace("|", ", "),
            "book_id": rating[3]
        } for rating in ratings]

        print(ratings)

        return list(sorted(ratings, key=lambda x: x["value"], reverse=True))


    def get_recommendations(self, num_recommendations=10):

        # Convert Book to a DataFrame
        books = pd.DataFrame([book.to_dict() for book in Book.query.all()])
        books = books.rename({"id": "book_id"}, axis=1)

        # Convert Rating to a DataFrame
        ratings = pd.DataFrame([rating.to_dict() for rating in Rating.query.all()])
        ratings = ratings.drop("id", axis=1)

        R_df = ratings.pivot_table(index="user_id", columns="book_id", values="value").fillna(0)

        # Normalise by each user's mean.
        R = R_df.values
        user_ratings_mean = np.mean(R, axis=1)
        R_demeaned = R - user_ratings_mean.reshape(-1, 1)

        k = min(R_demeaned.shape[0] - 1, 50)

        U, sigma, Vt = svds(R_demeaned, k=k)
        sigma = np.diag(sigma)

        predictions = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
        predictions_df = pd.DataFrame(predictions, columns=R_df.columns)

        user_predictions = pd.DataFrame(predictions_df.iloc[self.id].sort_values(ascending=False)).reset_index()
        user_predictions.columns = ["book_id", "value"]

        print("USER PREDICTIONS\n")
        print(user_predictions)

        user_ratings = ratings[ratings.user_id == self.id]
        user_full = user_ratings.merge(books, how='left', on='book_id').sort_values('value', ascending=False)

        # Remove books that the user has already rated
        books = books[~books['book_id'].isin(user_full['book_id'])]

        print("BOOKS\n")
        print(books)

        recommendations = books.merge(user_predictions, how='left', on='book_id').sort_values('value', ascending=False)
        recommendations = recommendations[~recommendations["value"].isna()].iloc[:num_recommendations]

        print(recommendations["value"].isna().sum())

        recommendations["genres"] = recommendations["genres"].str.replace("|", ", ")
        recommendations["value"] = recommendations["value"].map(round_rating)

        print("RECOMMENDATIONS\n")
        print(recommendations)
        # print(list(recommendations))

        return recommendations.to_dict("records")

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

        return '{} rated {} {} stars'.format(self.user_id, self.book_id, self.value)

    def to_dict(self):

        return {
            "id": self.id,
            "book_id": self.book_id,
            "user_id": self.user_id,
            "value": self.value
        }

class Book(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    genres = db.Column(db.String(200))

    def __repr__(self):

        return '{} ({})'.format(self.title, ", ".join(self.genres.split("|")))

    def to_dict(self):

        return {
            "id": self.id,
            "title": self.title,
            "genres": self.genres,
        }