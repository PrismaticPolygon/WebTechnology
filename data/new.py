import pandas as pd

df = pd.read_csv("D:/Dev/PycharmProjects/WebTechnology/data/raw/book_tags.csv")

# Ah. There's 1000000. That'll be the issue.
# But then we don't even need Tags...
# Lol. One day I'll get everything done in one go, and it will be glorious.

print(len(df))


# import numpy as np
# import os
# # It's 13GB. No idea HOW it's been kept in memory. Christ.
# # Maybe we should cut down on the number of users.
# # To... 1000.
#
# NUMBER_OF_USERS = 100
#
# def build_matrix():
#
#     if not os.path.exists("D:/Dev/PycharmProjects/WebTechnology/data/parsed/ratings_matrix.npy"):
#
#         ratings = pd.read_csv("D:/Dev/PycharmProjects/WebTechnology/data/raw/ratings.csv")
#
#         # Preference is described as user-item matrix.
#         # p_{12} is the user's preference on item 2. So we'll want a big old
#         # Instead, we have user vectors. Each is 10,000 'digits'.
#         # And we don't care about efficiency
#
#         ratings = ratings[ratings["user_id"] < NUMBER_OF_USERS]
#
#         ratings = ratings.set_index(["user_id", "book_id"])
#
#         matrix = np.zeros((NUMBER_OF_USERS + 1, 10000 + 1), dtype="uint8")
#
#         for (user_id, book_id), row in ratings.iterrows():
#
#
#
#             matrix[user_id, book_id] = row["rating"]
#
#         np.savetxt("D:/Dev/PycharmProjects/WebTechnology/data/parsed/ratings_matrix.npy", matrix)
#
#     else:
#
#         matrix = np.load(open("D:/Dev/PycharmProjects/WebTechnology/data/parsed/ratings_matrix.npy"))
#
#     return matrix
#
# # But it's still not what I'm after. At this rate, I'm going to have two concurrent systems.
#
# # Singular value decomposition decomposes the preference matrix as P_{m x n} = U_{m x m}
# # Only the non-miassing entries are considered.
#
# # Offline batch computing and online serving. Calculate easily fetchable recommendations offline by batch.
# # Reduce complexity by leveraging sparsity.
#
# # Yikes, that's slow.
#
#
# matrix = build_matrix()
#
#
#
#
#
