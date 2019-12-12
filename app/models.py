from hashlib import md5
import pandas as pd
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from scipy.sparse.linalg import svds
import numpy as np

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    ratings = db.relationship("Rating", backref="rater", lazy="dynamic")

    def __repr__(self):

        return '#{}: {}'.format(self.id, self.username)

    def get_ratings(self):

        ratings = self.ratings.order_by(Rating.value.desc()).join(Book).add_columns(Book.title, Book.genres, Book.id).all()

        ratings = [{
            "value": rating[0].value,
            "title": rating[1],
            "genres": rating[2].replace("|", ", "),
            "book_id": rating[3]
        } for rating in ratings]

        return ratings

    @staticmethod
    def build_matrices():

        # Convert Book to a DataFrame
        books_df = pd.DataFrame([book.to_dict() for book in Book.query.all()])
        books_df = books_df.rename({"id": "book_id"}, axis=1)

        print("BOOKS\n")
        print(books_df)

        # Convert Rating to a DataFrame
        ratings_df = pd.DataFrame([rating.to_dict() for rating in Rating.query.all()])
        ratings_df = ratings_df.drop("id", axis=1)

        print("RATINGS\n")
        print(ratings_df)

        R_df = ratings_df.pivot(index="user_id", columns="book_id", values="value").fillna(0)

        R = R_df.values
        user_ratings_mean = np.mean(R, axis=1)
        R_demeaned = R - user_ratings_mean.reshape(-1, 1)

        k = min(R_demeaned.shape[0] - 1, 25)

        U, sigma, Vt = svds(R_demeaned, k=k)
        sigma = np.diag(sigma)

        predictions = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
        predictions_df = pd.DataFrame(predictions, columns=R_df.columns)

        return predictions_df, books_df


    def get_recommendations(self, num_recommendations=10):

        predictions_df, books_df = User.build_matrices()

        ratings = pd.DataFrame([rating.to_dict() for rating in self.ratings.all()])

        if ratings.empty:    # Return some random books

            recommendations = books_df.sample(n=num_recommendations)

            recommendations["value"] = "No data available"
            recommendations["genres"] = recommendations["genres"].str.replace("|", ", ")

            return recommendations.to_dict("records")

        user_predictions = pd.DataFrame(predictions_df.iloc[self.id - 1].sort_values(ascending=False)).reset_index()
        user_predictions.columns = ["book_id", "value"]


        print("USER PREDICTIONS\n")
        print(user_predictions)

        user_full = ratings.merge(books_df, how='left', on='book_id').sort_values('value', ascending=False)

        # Remove books that the user has already rated
        books_df = books_df[~books_df['book_id'].isin(user_full['book_id'])]

        print("BOOKS\n")
        print(books_df)

        recommendations = books_df.merge(user_predictions, how='left', on='book_id').sort_values('value', ascending=False)
        recommendations = recommendations[~recommendations["value"].isna()].iloc[:num_recommendations]
        recommendations["genres"] = recommendations["genres"].str.replace("|", ", ")
        recommendations["value"] = recommendations["value"].map(lambda x: "{0:.2f}".format(x))

        print("RECOMMENDATIONS\n")
        print(recommendations)

        return recommendations.to_dict("records")

    def set_password(self, password):

        self.password_hash = generate_password_hash(password)

    def check_password(self, password):

        return check_password_hash(self.password_hash, password)

    def avatar(self, size):

        digest = md5(self.email.lower().encode('utf-8')).hexdigest()

        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

@login.user_loader
def load_user(id):

    return User.query.get(int(id))

class Rating(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    value = db.Column(db.Integer)

    def __repr__(self):

        return '#{}: user_{} rated book {} {}'.format(self.id, self.user_id, self.book_id, self.value)

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

        return '#{}: {} ({})'.format(self.id, self.title, ", ".join(self.genres.split("|")))

    def to_dict(self):

        return {
            "id": self.id,
            "title": self.title,
            "genres": self.genres,
        }