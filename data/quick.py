import pandas as pd

books = pd.read_csv("D:/Dev/PycharmProjects/WebTechnology/data/raw/books.csv")
book_tags = pd.read_csv("D:/Dev/PycharmProjects/WebTechnology/data/raw/book_tags.csv")

merge = pd.merge(books, book_tags, on="goodreads_book_id")

book_tags = merge[["book_id", "tag_id", "count"]]

book_tags.set_index("book_id", inplace=True)

book_tags.to_csv("D:/Dev/PycharmProjects/WebTechnology/data/parsed/book_tags.csv")
