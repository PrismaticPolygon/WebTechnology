import numpy as np
import pandas as pd
from scipy.sparse.linalg import svds

books = pd.read_csv("D:/Dev/PycharmProjects/WebTechnology/books.csv")
ratings = pd.read_csv("D:/Dev/PycharmProjects/WebTechnology/ratings.csv")

print(books.head())
print(ratings.head())

ratings.reset_index(inplace=True)

R_df = ratings.pivot_table(index="user_id", columns="book_id", values="value").fillna(0)

# Index contains duplicate entries....
# No user could have rating multiple books.

# One row per user, and one column per book.

print(R_df.head())

R = R_df.as_matrix()
user_ratings_mean = np.mean(R, axis = 1)
R_demeaned = R - user_ratings_mean.reshape(-1, 1)

# Interesting. It's 9 by 91. Of course: we only have 10 users, and apparently only 91 books actually got rated!

print(R_demeaned.shape)

U, sigma, Vt = svds(R_demeaned, k=5)

sigma = np.diag(sigma)

all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)

preds_df = pd.DataFrame(all_user_predicted_ratings, columns = R_df.columns)

# Nice.
# We could in theory generate this once and then leave it there.

userID = 1
num_recommendations = 5
sorted_user_predictions = preds_df.iloc[userID].sort_values(ascending=False)

user_data = ratings[ratings.user_id == userID]

user_full = (user_data.merge(books, how='left', left_on='book_id', right_on='book_id').sort_values(['value'], ascending=False))

print('User {0} has already rated {1} books.'.format(userID, user_full.shape[0]))
print('Recommending the highest {0} predicted ratings movies not already rated.'.format(num_recommendations))
#
# # Recommend the highest predicted rating movies that the user hasn't seen yet.
recommendations = (books[~books['book_id'].isin(user_full['book_id'])].
                       merge(pd.DataFrame(sorted_user_predictions).reset_index(), how='left',
                             left_on='book_id',
                             right_on='book_id').
                       rename(columns={userID: 'Predictions'}).
                       sort_values('Predictions', ascending=False).
                       iloc[:num_recommendations, :-1]
                       )

# All fairly dull values.
# I'll expand my genre preference scheme, I think.
# But the important thing: it works!
# There we go! That's a bit cooler.

print(preds_df.head())

print(sorted_user_predictions.head())

print(recommendations.head())


#
# GENRES = ['action', 'adventure', 'art', 'autobiography', 'anthology', 'biography', "childrens", 'cookbook',
#           'comic', 'diary', 'dictionary', 'crime', 'encyclopedia', 'drama', 'guide', 'fairytale', 'health',
#           'fantasy', 'history', 'graphic', 'journal', 'historical', 'math', 'horror', 'memoir', 'mystery', 'prayer',
#           'paranormal', 'religion', 'picture', 'textbook', 'poetry', 'review', 'political', 'crime', 'science',
#           'romance', 'satire', 'travel', 'scifi', 'short', 'suspense', 'thriller', 'ya', 'modern', 'classic',
#           'detective', 'war', 'period']
#
# # No idea why it's fucked.
#
# books = books.rename({"id": "book_id", "book_id": "title", "title": "action"}, axis=1)
# books = books.set_index("book_id")
#
# # Why do I have two titles?
#
# ratings = ratings.rename({"value": "rating"}, axis=1)
# ratings = ratings.drop(["id", "user_id"], axis=1)
# ratings = ratings.set_index("book_id")
#
# # print(books.head())
# # print(ratings.head())
#
# merged = pd.merge(books, ratings, on="book_id")
#
# user_genres = merged.drop(["title", "rating"], axis=1)
# user_ratings = ratings
#
# # user_genres.set_index("book_id", inplace=True)
#
# print(user_ratings)
# print(user_genres)
#
# profile = user_genres.T.dot(user_ratings.rating)
#
# books_with_genres = books.drop("title", axis=1)
#
# print(books_with_genres.head())
#
# # books_with_genres.set_index("book_id", inplace=True)
# # books_with_genres.drop(["title", "author", "year"], axis=1, inplace=True)
# #
# recommendations = (books_with_genres.dot(profile)) / profile.sum()
#
# recommendations.sort_values(ascending=False, inplace=True)
# #
# recommendations.rename("recommendation", inplace=True)
#
# print(recommendations.head())
# # # print(books.head())
# #
# data = pd.merge(books, recommendations, left_index=True, right_index=True)["title"]
# #
# # data.sort_values("recommendation", inplace=True, ascending=False)
# # data.drop("recommendation", inplace=True, axis=1)
# #
# # # print(user_ratings.user_id)
# #
# data.drop(user_ratings.index, inplace=True) # Remove books already rated by the user.
#
# print(list(data[:10]))
# #
# # return data.to_dict("records")
# #
# # # Pros: determines the user's preferences. Highly personalised to the user.
# # # Cons: doesn't take into account what others think of the item. Recommendations might be low-quality. No new genres
# # #       ever get recommended. But it's a start.
# #
# # from sklearn.metrics.pairwise import cosine_similarity
# #
# # root = "goodreads"
# #
# # books = pd.read_csv(root + "/books.csv")
# # ratings = pd.read_csv(root + "/ratings.csv", index_col=["user_id", "book_id"], dtype={"rating": "uint8"})
# #
# # mean = ratings.groupby(level=0).mean()
# #
# # ratings = ratings.join(mean, on="user_id", rsuffix="_mean")
# # ratings["rating_adjusted"] = (ratings["rating"] - ratings["rating_mean"])
# #
# # ratings.drop(["rating", "rating_mean"], axis=1, inplace=True)
# #
# # matrix = ratings.unstack(fill_value=0)
# #
# # print(matrix.info())
# #
# # print(matrix)
#
# # I wonder what state I left this in.
#
# # cosine_similarities = cosine_similarity(matrix)
# #
# # print(cosine_similarities.shape)
# # print(cosine_similarities)
#
# # print(cosine_similarity(matrix))
#
# # There we go!
# # User-based: use the rating matrix to find similar users based on the ratings they give
# # Item-based: use the rating matrix to find similar items based on the ratings given to them by users
#
#
# # In the user-item matrix, there are two dimensions: the number of users, and the number of items.
#
# # https://realpython.com/build-recommendation-engine-collaborative-filtering/
# # Row: ratings given by a user
# # Column: ratings received by an item
#
# # To find the rating R that a user U would give to an item I:
# #   Find users similar to U who have rated the item I
# #   Calculate the rating R based on the ratings of users found in the previous step
#
# # Remove biases by subtracting the average given by that user to all items from each item rated by that user