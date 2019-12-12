from time import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import User, Rating, Book
import csv
import pandas as pd
import random
import numpy as np

NUMBER_OF_USERS = 50

books = pd.read_csv("data/books.csv", index_col="book_id")

NUMBER_OF_BOOKS = len(books)
GENRES = []

NUMBER_OF_RATINGS = int(NUMBER_OF_BOOKS / 3)

for genres in books["genres"]:

    for genre in genres.split("|"):

        if genre not in GENRES:

            GENRES.append(genre)

NUMBER_OF_GENRES = len(GENRES)

def generate_users():

    users = list()

    for i in range(1, NUMBER_OF_USERS + 1):

        user = User(username="user_" + str(i), email="user_" + str(i) + "@email.com")
        user.set_password("password_" + str(i))

        users.append(user)

    return users

def round_rating(number):

    return round(number * 2) / 2

def generate_ratings():

    ratings = list()
    book_ids = range(1, NUMBER_OF_BOOKS)

    for user_id in range(1, NUMBER_OF_USERS):

        user_preferences = np.random.rand(NUMBER_OF_GENRES)

        for book_id in random.choices(book_ids, k=NUMBER_OF_RATINGS):

            book_genres = books.iloc[book_id].genres.split("|")

            value = 0

            for genre in book_genres:

                value += user_preferences[GENRES.index(genre)]

            value = round_rating((5 * value) / len(book_genres))

            rating = Rating(book_id=book_id, user_id=user_id, value=value)

            ratings.append(rating)

    with open("data/ratings.csv", "w", newline="") as ratings_file:

        writer = csv.DictWriter(ratings_file, fieldnames=["book_id", "user_id", "value"])
        writer.writeheader()

        for rating in ratings:

            writer.writerow({
                "user_id": rating.user_id,
                "book_id": rating.book_id,
                "value": rating.value
            })

    return ratings

def generate_books():

    _books = list()

    for index, (title, genres) in books.iterrows():

        book = Book(title=title, genres=genres)

        _books.append(book)

    return _books

if __name__ == "__main__":

    t = time()

    # Create the database
    engine = create_engine('sqlite:///app.db')

    generators = [
        generate_users,
        generate_ratings,
        generate_books
    ]

    for generator in generators:

        print("Running " + generator.__name__)

        t = time()

        # Create the session
        session = sessionmaker()
        session.configure(bind=engine)
        s = session()

        try:

            data = generator()

            s.bulk_save_objects(data)

            s.commit()

        except Exception as e:

            print("ERROR: ", e)

        finally:

            s.close()

        print("Time elapsed: {}s\n".format(str(time() - t)))  # 0.091s