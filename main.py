import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer

books = pd.read_csv("data/books.csv")
ratings = pd.read_csv("data/ratings.csv")

books["genres"] = books.genres.str.split("|")

mlb = MultiLabelBinarizer()

books = books.join(pd.DataFrame(mlb.fit_transform(books.pop('genres')),
                          columns=mlb.classes_,
                          index=books.index))


# print(books.head())
# print(ratings.head())

merged = pd.merge(books, ratings, on="book_id")

user_ratings = merged[["book_id", "title", "rating"]]
user_genres = merged.drop(["title", "user_id", "rating", "author", "year"], axis=1)

user_ratings.set_index("book_id", inplace=True)
user_genres.set_index("book_id", inplace=True)

# print(user_ratings.head())
# print(user_genres.head())
#
# print("Shape of ratings: {}".format(ratings.shape))
# print("Shape of genres: {}".format(ratings.shape))

profile = user_genres.T.dot(user_ratings.rating)

print(profile)

books.set_index("book_id", inplace=True)
books.drop(["title", "author", "year"], axis=1, inplace=True)

print(books.head())

recommendations = (books.dot(profile)) / profile.sum()
recommendations.sort_values(ascending=False, inplace=True)

print(recommendations.head())

# Pros: determines the user's preferences. Highly personalised to the user.
# Cons: doesn't take into account what others think of the item. Recommendations might be low-quality. No new genres
#       ever get recommended. But it's a start.

