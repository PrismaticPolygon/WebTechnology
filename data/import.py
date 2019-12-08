from time import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Book, BookTag, Rating, Tag, User
import csv
import pandas as pd

def load(file_name):

    with open(file_name, encoding="utf-8") as file:

        return [{k: v for k, v in row.items()} for row in csv.DictReader(file, skipinitialspace=True)]

def import_books():

    file_name = "D:/Dev/PycharmProjects/WebTechnology/data/parsed/books.csv"
    data = load(file_name)

    return list(map(lambda i: Book(**{
        "title": i["title"],
        "genres": "None"
    }), data))

def import_users():

    def make_user(i):

        i += 1

        user = User(username="user_" + str(i), email="user_" + str(i) + "@email.com")
        user.set_password("password_" + str(i))

        return user

    return list(map(lambda i: make_user(i), range(53424)))

def import_ratings():

    file_name = "D:/Dev/PycharmProjects/WebTechnology/data/parsed/ratings.csv"
    data = load(file_name)

    return list(map(lambda i: Rating(**{
        "book_id": int(i["book_id"]),
        "user_id": int(i["user_id"]),
        "value": int(i["rating"])
    }), data))

def import_tags():

    file_name = "D:/Dev/PycharmProjects/WebTechnology/data/raw/tags.csv"
    data = load(file_name)

    return list(map(lambda i: Tag(**{
        "name": i["tag_name"],
    }), data))

def import_book_tags():

    books = pd.read_csv("D:/Dev/PycharmProjects/WebTechnology/data/raw/books.csv")
    book_tags = pd.read_csv("D:/Dev/PycharmProjects/WebTechnology/data/raw/book_tags.csv")

    merge = pd.merge(books, book_tags, on="goodreads_book_id")[["book_id", "tag_id", "count"]]

    book_tags = list()

    for index, row in merge.itterows():

        book_tags.append(BookTag(book_id=row[0], tag_id=row[1], count=row[2]))

    return book_tags

if __name__ == "__main__":

    t = time()

    # Create the database
    engine = create_engine('sqlite:///app.db')

    import_functions = [
        import_books,
        import_users,
        import_ratings,
        import_tags,
        import_book_tags
    ]

    for import_function in import_functions:

        print("Running " + import_function.__name__)

        t = time()

        # Create the session
        session = sessionmaker()
        session.configure(bind=engine)
        s = session()

        try:

            data = import_function()

            s.bulk_save_objects(data)

            s.commit()

        except Exception as e:

            print("Error: ", e)

        finally:

            s.close()

        print("Time elapsed: {}s".format(str(time() - t)))  # 0.091s