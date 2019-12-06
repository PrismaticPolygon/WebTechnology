import pandas as pd
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
