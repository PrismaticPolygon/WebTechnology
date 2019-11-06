import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer

books = pd.read_csv("data/books.csv")
ratings = pd.read_csv("data/ratings.csv", index_col=["user_id", "book_id"])


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


def get_user_recommendations(user_id):

    user_ratings = ratings.loc[(user_id,)]
    user_genres = merged.drop(["title", "rating", "author", "year"], axis=1)

    # user_ratings.set_index("book_id", inplace=True)
    user_genres.set_index("book_id", inplace=True)

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