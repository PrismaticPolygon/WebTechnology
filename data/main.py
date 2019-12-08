import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer

books = pd.read_csv("C:/Users/user/PycharmProjects/WebTechnology/data/books.csv")
ratings = pd.read_csv("C:/Users/user/PycharmProjects/WebTechnology/data/ratings.csv", index_col=["user_id", "book_id"])

def create_rating(user_id, book_id, rating):

    ratings.loc[(user_id, book_id), ['rating']] = [rating]

def read_rating(user_id, book_id):

    return ratings.at[(user_id, book_id), "rating"]

def update_rating(user_id, book_id, rating):

    ratings.loc[(user_id, book_id), ['rating']] = [rating]

def delete_rating(user_id, book_id):

    ratings.drop((user_id, book_id), inplace=True)


books["genres"] = books.genres.str.split("|")

mlb = MultiLabelBinarizer()

books_with_genres = books.join(pd.DataFrame(mlb.fit_transform(books.pop('genres')),
                                                        columns=mlb.classes_,
                                                        index=books.index))

books.set_index("book_id", inplace=True)

merged = pd.merge(books_with_genres, ratings, on="book_id")

def get_user_ratings(user_id):

    user_ratings = ratings.loc[(user_id,)]

    return pd.merge(books, user_ratings, left_index=True, right_index=True).to_dict("records")

# Ah. It seems to be too large.

def get_user_recommendations(user_id):

    user_ratings = ratings.loc[(user_id,)]
    user_genres = merged.drop(["title", "rating", "author", "year"], axis=1)

    # Matrices are not aligned.

    user_genres.set_index("book_id", inplace=True)

    print(user_ratings)
    print(user_genres)

    profile = user_genres.T.dot(user_ratings.rating)

    books_with_genres.set_index("book_id", inplace=True)
    books_with_genres.drop(["title", "author", "year"], axis=1, inplace=True)

    recommendations = (books_with_genres.dot(profile)) / profile.sum()
    recommendations.sort_values(ascending=False, inplace=True)

    recommendations.rename("recommendation", inplace=True)

    # print(recommendations.head())
    # print(books.head())

    data = pd.merge(books, recommendations, left_index=True, right_index=True)

    # print(list(data))

    data.sort_values("recommendation", inplace=True, ascending=False)
    data.drop("recommendation", inplace=True, axis=1)

    # print(user_ratings.user_id)

    data.drop(user_ratings.index, inplace=True) # Remove books already rated by the user.

    return data.to_dict("records")

# Pros: determines the user's preferences. Highly personalised to the user.
# Cons: doesn't take into account what others think of the item. Recommendations might be low-quality. No new genres
#       ever get recommended. But it's a start.

from sklearn.metrics.pairwise import cosine_similarity

root = "goodreads"

books = pd.read_csv(root + "/books.csv")
ratings = pd.read_csv(root + "/ratings.csv", index_col=["user_id", "book_id"], dtype={"rating": "uint8"})

mean = ratings.groupby(level=0).mean()

ratings = ratings.join(mean, on="user_id", rsuffix="_mean")
ratings["rating_adjusted"] = (ratings["rating"] - ratings["rating_mean"])

ratings.drop(["rating", "rating_mean"], axis=1, inplace=True)

matrix = ratings.unstack(fill_value=0)

print(matrix.info())

print(matrix)

# I wonder what state I left this in.

# cosine_similarities = cosine_similarity(matrix)
#
# print(cosine_similarities.shape)
# print(cosine_similarities)

# So we want to get

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
