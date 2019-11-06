import pandas as pd
import functools

books = pd.read_csv("raw/books.csv", index_col="goodreads_book_id")
book_tags = pd.read_csv("raw/book_tags.csv")
tags = pd.read_csv("raw/tags.csv", index_col="tag_id")

book_tags = book_tags.merge(tags, on="tag_id")

stop_tags = ["owned", "books-i-own", "to-buy", "default", "wish-list", "i-own", "own-it", "bought",
             "abandoned", "to-get", "audible", "on-hold", "recommended", "scanned", "and",
             "maybe", "have", "borrowed", "collection", "gave-up", "do-not-own"
             "on-my-shelf", "series", "author", "mine"]
exclude = ["read", "audio", "kindle", "book", "library", "favorite", "favourite", "star", "favs", "finish", "collection",
           "wishlist", "shelf", "buy"]

book_tags = book_tags.query('tag_name not in {}'.format(stop_tags))
book_tags = book_tags.set_index("goodreads_book_id")

# Then split by "-".


for word in exclude:

    book_tags = book_tags[~book_tags["tag_name"].str.contains(word)]

genres = pd.DataFrame(index=book_tags.index.unique())
genres["genres"] = ""
genres.index.name = "goodreads_book_id"

for index in list(book_tags.index.unique()):

    tags = book_tags.loc[index].sort_values("count")[:10]

    genres.at[index, "genres"] = functools.reduce(lambda acc, cur: acc + "|" + cur, tags["tag_name"])

books = books.join(genres)
books = books[["title", "authors", "genres", "book_id"]]
books = books.set_index("book_id")

books.to_csv("data/books.csv")