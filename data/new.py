import pandas as pd
import numpy as np
import os

# It's 13GB. No idea HOW it's been kept in memory. Christ.
# Maybe we should cut down on the number of users.
# To... 1000.

def build_matrix():

    if not os.path.exists("D:/Dev/PycharmProjects/WebTechnology/data/raw/ratings_matrix.npy"):

        ratings = pd.read_csv("D:/Dev/PycharmProjects/WebTechnology/data/raw/ratings.csv", index_col=["user_id", "book_id"])

        # Preference is described as user-item matrix.
        # p_{12} is the user's preference on item 2. So we'll want a big old
        # Instead, we have user vectors. Each is 10,000 'digits'.
        # And we don't care about efficiency

        matrix = np.zeros((53424 + 1, 10000 + 1))

        for (user_id, book_id), row in ratings.iterrows():

            matrix[user_id, book_id] = row["rating"]

        np.savetxt("D:/Dev/PycharmProjects/WebTechnology/data/raw/ratings_matrix.npy", matrix)

    else:

        matrix = np.load(open("D:/Dev/PycharmProjects/WebTechnology/data/raw/ratings_matrix.npy"))

    return matrix

# Singular value decomposition decomposes the preference matrix as P_{m x n} = U_{m x m}
# Only the non-miassing entries are considered.

# Offline batch computing and online serving. Calculate easily fetchable recommendations offline by batch.
# Reduce complexity by leveraging sparsity.

# Yikes, that's slow.


matrix = build_matrix()



# Now we just populate the matrix.
# It's so hard to think in vectorised form.

print(ratings.head())




