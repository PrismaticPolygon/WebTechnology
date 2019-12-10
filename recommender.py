from app import db
from app.models import Book, User


import pandas as pd
#
books = pd.read_csv("D:/Dev/PycharmProjects/WebTechnology/books.csv")
ratings = pd.read_csv("D:/Dev/PycharmProjects/WebTechnology/ratings.csv")

GENRES = ['action', 'adventure', 'art', 'autobiography', 'anthology', 'biography', "childrens", 'cookbook',
          'comic', 'diary', 'dictionary', 'crime', 'encyclopedia', 'drama', 'guide', 'fairytale', 'health',
          'fantasy', 'history', 'graphic', 'journal', 'historical', 'math', 'horror', 'memoir', 'mystery', 'prayer',
          'paranormal', 'religion', 'picture', 'textbook', 'poetry', 'review', 'political', 'crime', 'science',
          'romance', 'satire', 'travel', 'scifi', 'short', 'suspense', 'thriller', 'ya', 'modern', 'classic',
          'detective', 'war', 'period']

# No idea why it's fucked.

books = books.rename({"id": "book_id", "book_id": "title", "title": "action"}, axis=1)
books = books.set_index("book_id")

# Why do I have two titles?

ratings = ratings.rename({"value": "rating"}, axis=1)
ratings = ratings.drop(["id", "user_id"], axis=1)
ratings = ratings.set_index("book_id")

# print(books.head())
# print(ratings.head())

merged = pd.merge(books, ratings, on="book_id")

user_genres = merged.drop(["title", "rating"], axis=1)
user_ratings = ratings

# user_genres.set_index("book_id", inplace=True)

print(user_ratings)
print(user_genres)

profile = user_genres.T.dot(user_ratings.rating)

books_with_genres = books.drop("title", axis=1)

print(books_with_genres.head())

# books_with_genres.set_index("book_id", inplace=True)
# books_with_genres.drop(["title", "author", "year"], axis=1, inplace=True)
#
recommendations = (books_with_genres.dot(profile)) / profile.sum()

recommendations.sort_values(ascending=False, inplace=True)
#
recommendations.rename("recommendation", inplace=True)

print(recommendations.head())
# # print(books.head())
#
data = pd.merge(books, recommendations, left_index=True, right_index=True)["title"]
#
# data.sort_values("recommendation", inplace=True, ascending=False)
# data.drop("recommendation", inplace=True, axis=1)
#
# # print(user_ratings.user_id)
#
data.drop(user_ratings.index, inplace=True) # Remove books already rated by the user.

print(list(data[:10]))
#
# return data.to_dict("records")
#
# # Pros: determines the user's preferences. Highly personalised to the user.
# # Cons: doesn't take into account what others think of the item. Recommendations might be low-quality. No new genres
# #       ever get recommended. But it's a start.
#
# from sklearn.metrics.pairwise import cosine_similarity
#
# root = "goodreads"
#
# books = pd.read_csv(root + "/books.csv")
# ratings = pd.read_csv(root + "/ratings.csv", index_col=["user_id", "book_id"], dtype={"rating": "uint8"})
#
# mean = ratings.groupby(level=0).mean()
#
# ratings = ratings.join(mean, on="user_id", rsuffix="_mean")
# ratings["rating_adjusted"] = (ratings["rating"] - ratings["rating_mean"])
#
# ratings.drop(["rating", "rating_mean"], axis=1, inplace=True)
#
# matrix = ratings.unstack(fill_value=0)
#
# print(matrix.info())
#
# print(matrix)

# I wonder what state I left this in.

# cosine_similarities = cosine_similarity(matrix)
#
# print(cosine_similarities.shape)
# print(cosine_similarities)

# print(cosine_similarity(matrix))

# There we go!
# User-based: use the rating matrix to find similar users based on the ratings they give
# Item-based: use the rating matrix to find similar items based on the ratings given to them by users


# In the user-item matrix, there are two dimensions: the number of users, and the number of items.

# https://realpython.com/build-recommendation-engine-collaborative-filtering/
# Row: ratings given by a user
# Column: ratings received by an item

# To find the rating R that a user U would give to an item I:
#   Find users similar to U who have rated the item I
#   Calculate the rating R based on the ratings of users found in the previous step

# Remove biases by subtracting the average given by that user to all items from each item rated by that user