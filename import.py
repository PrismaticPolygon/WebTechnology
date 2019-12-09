from time import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Book, BookTag, Rating, Tag, User
import csv
import pandas as pd

NUMBER_OF_BOOKS = 10000
NUMBER_OF_USERS = 100
TAG_MAP = dict()    # Holds a map: old tag_id to a list of tag_ids

# https://reference.yourdictionary.com/books-literature/different-types-of-books.html. There are 44.
GENRES = ['action', 'adventure', 'art', 'autobiography', 'anthology', 'biography', "childrens", 'cookbook',
              'comic', 'diary', 'dictionary', 'crime', 'encyclopedia', 'drama', 'guide', 'fairytale', 'health',
              'fantasy', 'history', 'graphic', 'journal', 'historical', 'math', 'horror', 'memoir', 'mystery', 'prayer',
              'paranormal', 'religion', 'picture', 'textbook', 'poetry', 'review', 'political', 'crime', 'science',
              'romance', 'satire', 'travel', 'scifi', 'short', 'suspense', 'thriller', 'ya', 'modern', 'classic',
              'detective', 'war', 'period']

def load(file_name):
    """
    Load a file into a list of dictionaries
    """

    with open(file_name, encoding="utf-8") as file:

        return [{k: v for k, v in row.items()} for row in csv.DictReader(file, skipinitialspace=True)]

def write(file_name, data):
    """
    Write a db.Model object with a to_dict function to a CSV
    """

    print(data[0].to_dict())

    # id is None. Of course.

    keys = list(data[0].to_dict().keys())

    with open(file_name, "w", newline="") as file:

        writer = csv.DictWriter(file, fieldnames=keys)

        writer.writerow(keys)

        for item in data:

            item = item.to_dict()
            item["id"] = item.username.split("_")[0]

            print(item)

            writer.writerow(item.to_dict())

def import_books():

    build_tag_map()
    #
    # print(TAG_MAP)

    books = pd.read_csv("D:/Dev/PycharmProjects/WebTechnology/data/raw/books.csv")

    books["genres"] = ""

    book_tags = pd.read_csv("D:/Dev/PycharmProjects/WebTechnology/data/raw/book_tags.csv")

    merge = pd.merge(books, book_tags, on="goodreads_book_id")[["book_id", "tag_id", "title"]]

    # Chill.

    # print(merge.head())

    # Very first book is missing data. Why?

    for index in range(NUMBER_OF_BOOKS + 1):

        tags = list()

        for tag in merge[merge["book_id"] == index]["tag_id"].values:
    #
            if tag in TAG_MAP:

                for id in TAG_MAP[tag]:

                    if GENRES[id] not in tags:

                        tags.append(GENRES[id])

        books.at[index, "genres"] = "|".join(tags)
    # #
    #     print(books.loc[index]["genres"])

    # for index, row in merge.iterrows():
    #
    #     tag_id = row[1]
    #
    #     if tag_id in TAG_MAP:
    #
    #         for tag in TAG_MAP[tag_id]:
    #
    #             books.at[index, tag] = 1

    # print(books.head())

    # book_tags = pd.read_csv("D:/Dev/PycharmProjects/WebTechnology/data/parsed/book_tags.csv", index_col="tag_id")
    # tags = pd.read_csv("D:/Dev/PycharmProjects/WebTechnology/data/parsed/tags.csv", index_col="tag_id")
    #
    # # Merge tags and book_tags on tag_id. Resulting table has book_id, tag_id, count, and tag_name
    #
    # book_tags = book_tags.merge(tags, on="tag_id")
    #
    # book_tags.reset_index()
    #
    # book_tags = book_tags.set_index("book_id")
    #
    # print(book_tags.head())
    #
    # for index in range(NUMBER_OF_BOOKS):
    #
    #     for tag in book_tags.loc[index]:
    #
    #         books[index][tag] = 1
    #
    # print(books.head())

    # books.to_csv("parsed/books.csv")

    return list(map(lambda i: Book(**{
        "title": i["title"],
        "genres": i["genres"]
    }), books.to_dict("record")))

def import_users():

    users = list()

    for i in range(1, NUMBER_OF_USERS + 1):

        user = User(username="user_" + str(i), email="user_" + str(i) + "@email.com")
        user.set_password("password_" + str(i))

        users.append(user)

    # write("D:/Dev/PycharmProjects/WebTechnology/data/parsed/users.csv", users)

    return users

def import_ratings():

    file_name = "D:/Dev/PycharmProjects/WebTechnology/data/raw/ratings.csv"
    data = load(file_name)

    ratings = list()

    for i in data:

        if int(i["user_id"]) < NUMBER_OF_USERS:

            rating = Rating(**{
                "book_id": int(i["book_id"]),
                "user_id": int(i["user_id"]),
                "value": int(i["rating"])
            })

            ratings.append(rating)

    # write("D:/Dev/PycharmProjects/WebTechnology/data/parsed/ratings.csv", ratings)

    return ratings

def build_tag_map():

    file_name = "D:/Dev/PycharmProjects/WebTechnology/data/raw/tags.csv"
    data = load(file_name)

    for index, item in enumerate(data):

        names = [x for x in item["tag_name"].split("-") if x != "" and not x.isdigit()]

        for name in names:

            if name in GENRES:

                if index not in TAG_MAP:

                    TAG_MAP[index] = [GENRES.index(name)]

                else:

                    TAG_MAP[index].append(GENRES.index(name))


def import_tags():

    file_name = "D:/Dev/PycharmProjects/WebTechnology/data/raw/tags.csv"
    data = load(file_name)

    tags = list()

    for index, item in enumerate(data):

        # Perhaps perhaps
        # Each should map too many, perhaps

        names = [x for x in item["tag_name"].split("-") if x != "" and not x.isdigit()]

        for name in names:

            if name in GENRES:

                tag =  Tag(**{
                    "name": name
                })

                # Should there be repeats? No.

                if index not in TAG_MAP:

                    TAG_MAP[index] = [GENRES.index(name)]

                else:

                    TAG_MAP[index].append(GENRES.index(name))

                if tag not in tags:

                    tags.append(tag)

    # write("D:/Dev/PycharmProjects/WebTechnology/data/parsed/tags.csv", tags)

    return tags

def import_book_tags():

    books = pd.read_csv("D:/Dev/PycharmProjects/WebTechnology/data/raw/books.csv")
    book_tags = pd.read_csv("D:/Dev/PycharmProjects/WebTechnology/data/raw/book_tags.csv")

    merge = pd.merge(books, book_tags, on="goodreads_book_id")[["book_id", "tag_id", "count"]]

    # Filter out tags that we've nuked.
    merge = merge[merge.tag_id.isin(TAG_MAP.keys())]

    # Replace the old tag id with the new tag id
    merge["tag_id"] = merge["tag_id"].map(lambda x: TAG_MAP[x])

    # Cause it means that we have multiple. Fortunately, we don't actually need them anyway,

    # merge.to_csv("D:/Dev/PycharmProjects/WebTechnology/data/parsed/book_tags.csv")

    book_tags = list()

    for index, row in merge.iterrows():

        book_tags.append(BookTag(book_id=row[0], tag_id=row[1], count=row[2]))

    return book_tags

if __name__ == "__main__":

    t = time()

    # Create the database
    engine = create_engine('sqlite:///app.db')

    import_functions = [
        import_users,
        import_ratings,
        # import_tags,
        # import_book_tags,
        import_books,
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

            print("ERROR: ", e)

        finally:

            s.close()

        print("Time elapsed: {}s\n".format(str(time() - t)))  # 0.091s