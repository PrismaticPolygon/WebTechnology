from time import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Book, BookTag, Rating, Tag
import csv

def load(file_name):

    with open(file_name, encoding="utf-8") as file:

        a = [{k: v for k, v in row.items()}
             for row in csv.DictReader(file, skipinitialspace=True)]

    return a

def import_book_tags():

    t = time()

    # Create the database
    engine = create_engine('sqlite:///app.db')

    # Create the session
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    try:

        # Interesting. How do I pass in a book?

        file_name = "D:/Dev/PycharmProjects/WebTechnology/data/parsed/book_tags.csv"  # sample CSV file used:  http://www.google.com/finance/historical?q=NYSE%3AT&ei=W4ikVam8LYWjmAGjhoHACw&output=csv
        data = load(file_name)

        for i in data:
            # Okay. There we go.

            print(i)

            record = BookTag(**{
                "book_id": int(i["book_id"]),
                "tag_id": int(i["tag_id"]),
                "count": int(i["count"])
            })

            #     record = Book(**{
            #         'date' : datetime.strptime(i[0], '%d-%b-%y').date(),
            #         'opn' : i[1],
            #         'hi' : i[2],
            #         'lo' : i[3],
            #         'close' : i[4],
            #         'vol' : i[5]
            #     })
            #
            s.add(record)  # Add all the records

        s.commit()  # Attempt to commit all the records

    except Exception as e:

        print(e)

        s.rollback()  # Rollback the changes on error

    finally:
        s.close()  # Close the connection

    print("Time elapsed: {}s".format(str(time() - t)))  # 0.091s

def import_ratings():

    t = time()

    # Create the database
    engine = create_engine('sqlite:///app.db')

    # Create the session
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    try:

        # Interesting. How do I pass in a book?

        file_name = "D:/Dev/PycharmProjects/WebTechnology/data/parsed/ratings.csv"  # sample CSV file used:  http://www.google.com/finance/historical?q=NYSE%3AT&ei=W4ikVam8LYWjmAGjhoHACw&output=csv
        data = load(file_name)

        records = list(map(lambda i: Rating(**{
                "book_id": int(i["book_id"]),
                "user_id": int(i["user_id"]),
                "value": int(i["rating"])
            }), data))

        s.bulk_save_objects(records)

        s.commit()  # Attempt to commit all the records

    except Exception as e:

        print(e)

        s.rollback()  # Rollback the changes on error

    finally:
        s.close()  # Close the connection

    print("Time elapsed: {}s".format(str(time() - t)))  # 0.091s

def import_tags():

    t = time()

    # Create the database
    engine = create_engine('sqlite:///app.db')

    # Create the session
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    try:

        # Interesting. How do I pass in a book?

        file_name = "D:/Dev/PycharmProjects/WebTechnology/data/raw/tags.csv"  # sample CSV file used:  http://www.google.com/finance/historical?q=NYSE%3AT&ei=W4ikVam8LYWjmAGjhoHACw&output=csv
        data = load(file_name)

        records = list(map(lambda i: Tag(**{
                # "tag_id": int(i["tag_id"]),
                "name": i["tag_name"],
            }), data))

        s.bulk_save_objects(records)

        s.commit()  # Attempt to commit all the records

    except Exception as e:

        print(e)

        s.rollback()  # Rollback the changes on error

    finally:
        s.close()  # Close the connection

    print("Time elapsed: {}s".format(str(time() - t)))  # 0.091s
# Now we just construct a user_table, I guess.
# Random passwords and IDs. Range is continguous.

if __name__ == "__main__":

    # import_book_tags()

    # Great. There's too many ratings

    # import_ratings()

    import_tags()
    # t = time()
    #
    # #Create the database
    # engine = create_engine('sqlite:///app.db')
    #
    # #Create the session
    # session = sessionmaker()
    # session.configure(bind=engine)
    # s = session()
    #
    # try:
    #
    #     # Interesting. How do I pass in a book?
    #
    #     file_name = "D:/Dev/PycharmProjects/WebTechnology/data/parsed/books.csv" #sample CSV file used:  http://www.google.com/finance/historical?q=NYSE%3AT&ei=W4ikVam8LYWjmAGjhoHACw&output=csv
    #     data = load(file_name)
    #
    #     for i in data:
    #
    #         # Okay. There we go.
    #
    #         print(i)
    #
    #         record = Book(**{
    #             "title": i["title"],
    #             "genres": "None"
    #         })
    #
    #     #     record = Book(**{
    #     #         'date' : datetime.strptime(i[0], '%d-%b-%y').date(),
    #     #         'opn' : i[1],
    #     #         'hi' : i[2],
    #     #         'lo' : i[3],
    #     #         'close' : i[4],
    #     #         'vol' : i[5]
    #     #     })
    #     #
    #         s.add(record) #Add all the records
    #
    #     s.commit() #Attempt to commit all the records
    #
    # except Exception as e:
    #
    #     print(e)
    #
    #     s.rollback() #Rollback the changes on error
    #
    # finally:
    #     s.close() #Close the connection
    #
    #
    # print("Time elapsed: {}s".format(str(time() - t))) #0.091s