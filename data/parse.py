import pandas as pd
import functools
import shutil

NUMBER_OF_BOOKS = 10000
NUMBER_OF_USERS = 100
TAG_MAP = dict()    # Holds a map: old tag_id to new tag_id.
GENRES = ['action', 'adventure', 'art', 'autobiography', 'anthology', 'biography', "childrens", 'cookbook',
          'comic', 'diary', 'dictionary', 'crime', 'encyclopedia', 'drama', 'guide', 'fairytale', 'health',
          'fantasy', 'history', 'graphic', 'journal', 'historical', 'math', 'horror', 'memoir', 'mystery', 'prayer',
          'paranormal', 'religion', 'picture', 'textbook', 'poetry', 'review', 'political', 'crime', 'science',
          'romance', 'satire', 'travel', 'scifi', 'short', 'suspense', 'thriller', 'ya']

books = pd.read_csv("raw/books.csv", index_col="goodreads_book_id", usecols=["book_id", "goodreads_book_id", "title"])
book_tags = pd.read_csv("raw/book_tags.csv")
tags = pd.read_csv("raw/tags.csv", index_col="tag_id")

# book_id, tag_id, and count
book_tags =  pd.merge(books, book_tags, on="goodreads_book_id")[["book_id", "tag_id", "count"]]

book_tags

# Loads of them are the same........... Which we kinda expected.

print(book_tags)

tag_list = list()

for index, row in tags.iterrows():

    name = row["tag_name"].split("-")[0]

    if name in GENRES:

        if name in tag_list:

            TAG_MAP[index][]


        tag_list.append(name)
        TAG_MAP[index] = len(tag_list)

tags = pd.DataFrame(tag_list)

print(tags)
# Remove exclusion words
#
# for genre in GENRES:
#
#     book_tags = book_tags[book_tags["tag_name"].str.equals(genre)]
#
# print(book_tags.head())
#
# # Build a genres table indexed by goodreads_book_id (i.e. 1 - 10000)
#
# genres = pd.DataFrame(index=book_tags.index.unique())
# genres["genres"] = ""
# genres.index.name = "goodreads_book_id"
#
# # Iterate through every goodreads_book_id. For each, get the 10 most popular tags, and create an array from those tags.
# # Save that array to the index of the book in question.
#
# for index in list(book_tags.index.unique()):
#
#     tags = book_tags.loc[index].sort_values("count")[:10]
#
#     genres.at[index, "genres"] = functools.reduce(lambda acc, cur: acc + "|" + cur, tags["tag_name"])
#
# print(genres.head())
#
# books = books.join(genres)
# books = books[["book_id", "title", "genres"]]
# books = books.set_index("book_id")
#
# books.to_csv("goodreads/books.csv")
#
# shutil.move("raw/ratings.csv", "goodreads/ratings.csv")
#
