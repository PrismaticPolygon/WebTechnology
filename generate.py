from time import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import User, Rating, Book
import pandas as pd
import random
import numpy as np
from config import Config

NUMBER_OF_USERS = 50
NUMBER_OF_BOOKS = 100
NUMBER_OF_GENRES = 41
MIN_NUMBER_OF_RATINGS = 10
MAX_NUMBER_OF_RATINGS = 50

GENRES = ['Action', 'Adult', 'Adult Fiction', 'Adventure', 'Animals', 'Biography', 'Childrens', 'Comics',
          'Contemporary', 'Crime', 'Death', 'Dystopia', 'Environment', 'Family', 'Fantasy', 'Fiction', 'Food and Drink',
          'Graphic Novels', 'Health', 'Historical Fiction', 'History', 'Horror', 'Humor', 'LGBT', 'Literary Fiction',
          'Memoir', 'Music', 'Mystery', 'Mythology', 'Nonfiction', 'Parenting', 'Picture Books', 'Poetry', 'Politics',
          'Romance', 'Science', 'Science Fiction', 'Self Help', 'Thriller', 'War', 'Young Adult']

books_df = pd.read_csv("data/books.csv", index_col="id")

def generate_users():

    users = list()

    for i in range(1, NUMBER_OF_USERS + 1):

        user = User(username="user_" + str(i), email="user_" + str(i) + "@email.com")
        user.set_password("password_" + str(i))

        users.append(user)

    return users

def generate_ratings():

    ratings = list()

    # Iterate through each user
    for user_id in range(1, NUMBER_OF_USERS + 1):

        # Generate a random genre preference array
        user_preferences = np.random.rand(NUMBER_OF_GENRES)

        n = random.randint(MIN_NUMBER_OF_RATINGS, MAX_NUMBER_OF_RATINGS)

        # Iterate over a random sample of n books
        for book_id, (title, genres) in books_df.sample(n).iterrows():

            book_genres = genres.split("|")
            value = 0

            for genre in book_genres:

                value += user_preferences[GENRES.index(genre)]

            # Convert to a half-decimal between 0 and 5
            value = round(2 * (5 * value) / len(book_genres)) / 2

            rating = Rating(book_id=book_id, user_id=user_id, value=value)

            ratings.append(rating)

    return ratings

def generate_books():

    books = list()

    for index, (title, genres) in books_df.iterrows():

        book = Book(title=title, genres=genres)

        books.append(book)

    return books

if __name__ == "__main__":

    config = Config()
    t = time()

    # Create the database
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)

    generators = [
        generate_users,
        generate_books,
        generate_ratings
    ]



    for generator in generators:

        print("Running " + generator.__name__ + "...", end="")

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

        print("DONE ({}s)".format(str(time() - t)))  # 0.091s