from time import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import User, Rating, Book
import csv
import pandas as pd
import random

NUMBER_OF_USERS = 10
books = pd.read_csv("D:/Dev/PycharmProjects/WebTechnology/books.csv", index_col="book_id")

GENRES = []
NUMBER_OF_BOOKS = len(books)

NUMBER_OF_RATINGS = int(NUMBER_OF_BOOKS / 4)

for genres in books["genres"]:

    for genre in genres.split("|"):

        if genre not in GENRES:

            GENRES.append(genre)

def generate_users():

    users = list()

    for i in range(1, NUMBER_OF_USERS + 1):

        user = User(username="user_" + str(i), email="user_" + str(i) + "@email.com")
        user.set_password("password_" + str(i))

        users.append(user)

    return users

def generate_ratings():

    ratings = list()
    book_ids = range(1, NUMBER_OF_BOOKS)

    for user_id in range(1, NUMBER_OF_USERS):

        best_genre = random.choice(GENRES)

        while 1:

            worst_genre = random.choice(GENRES)

            if worst_genre != best_genre:

                break

        for book_id in random.choices(book_ids, k=NUMBER_OF_RATINGS):

            book_genres = books.iloc[book_id].genres.split("|")

            value = random.choice([2, 3])

            if best_genre in book_genres:

                value = random.choice([4, 5])

            if worst_genre in book_genres:

                value = max(1, value - random.choice([2, 3]))

            rating = Rating(book_id=book_id, user_id=user_id, value=value)

            ratings.append(rating)


    with open("ratings.csv", "w", newline="") as ratings_file:

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

            print(data)

            # s.bulk_save_objects(data)
            #
            # s.commit()

        except Exception as e:

            print("ERROR: ", e)

        finally:

            s.close()

        print("Time elapsed: {}s\n".format(str(time() - t)))  # 0.091s