import pandas as pd
import functools
import shutil

# Load the datasets that we need

# These basically define relationships, right?

books = pd.read_csv("raw/books.csv", index_col="goodreads_book_id")
book_tags = pd.read_csv("raw/book_tags.csv")
tags = pd.read_csv("raw/tags.csv", index_col="tag_id")

# Merge tags and book_tags on tag_id. Resulting table has goodreads_book_id, tag_id, count, and tag_name

book_tags = book_tags.merge(tags, on="tag_id")

print(book_tags.head())

stop_tags = ["owned", "books-i-own", "to-buy", "default", "wish-list", "i-own", "own-it", "bought",
             "abandoned", "to-get", "audible", "on-hold", "recommended", "scanned", "and",
             "maybe", "have", "borrowed", "collection", "gave-up", "do-not-own"
             "on-my-shelf", "series", "author", "mine"]
exclude = ["read", "audio", "kindle", "book", "library", "favorite", "favourite", "star", "favs", "faves", "finish", "collection",
           "wishlist", "shelf", "buy", "summer", "review"]

# Remove stop tags, and set the index to goodreads_book_id

book_tags = book_tags.query('tag_name not in {}'.format(stop_tags))
book_tags = book_tags.set_index("goodreads_book_id")

# Remove exclusion words

for word in exclude:

    book_tags = book_tags[~book_tags["tag_name"].str.contains(word)]

print(book_tags.head())

# Build a genres table indexed by goodreads_book_id (i.e. 1 - 10000)

genres = pd.DataFrame(index=book_tags.index.unique())
genres["genres"] = ""
genres.index.name = "goodreads_book_id"

# Iterate through every goodreads_book_id. For each, get the 10 most popular tags, and create an array from those tags.
# Save that array to the index of the book in question.

for index in list(book_tags.index.unique()):

    tags = book_tags.loc[index].sort_values("count")[:10]

    genres.at[index, "genres"] = functools.reduce(lambda acc, cur: acc + "|" + cur, tags["tag_name"])

print(genres.head())

books = books.join(genres)
books = books[["book_id", "title", "genres"]]
books = books.set_index("book_id")

books.to_csv("goodreads/books.csv")

shutil.move("raw/ratings.csv", "goodreads/ratings.csv")