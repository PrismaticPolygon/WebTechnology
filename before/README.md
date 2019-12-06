




### Data

The dataset is from Goodreads, a social book cataloguing site. It comprises 6 million ratings for 
the then thousand most popular books, along with book metadata. It can be found [here](https://github.com/zygmuntz/goodbooks-10k).

It contains four tables of interest:
1. `ratings.csv` comprises `user_id`, `book_id`, and `rating` (between 1 and 5). Both `user_id` and `book_id` are
contiguous (between 1 - 53424 for users, and 1 - 10000 for books).
2. `books.csv` has metadata for each book, such as `goodread_book_id`, `authors`, `title`, `isbn`, and so on.
3. `book_tags.csv` contains tags / shelves / genres assigned by users to books, represented by their `tag_id`.
4. `tags.csv` comprises `tag_id`, and `tag_name`. 

#### Pre-processing

It is specified in the assignment that the database should consist of two tables:
1. UserID, BookID, Rating
2. BookID, Title, Genres

So a lot of fields can be removed.

Tags roughly correspond to genres in this dataset, though, as they are user-defined, plenty
are useless, and so are removed in `parse.py`.

### Recommended links

* https://stackabuse.com/creating-a-simple-recommender-system-in-python-using-pandas/
* https://beckernick.github.io/matrix-factorization-recommender/
* https://www.makeuseof.com/tag/python-javascript-communicate-json/

### Notes
* Rating should be dynamically updated as users make updates
* Users should be able to log in, with tokens stored in cookies
* Interaction is more important than layout
* Best way to submit is to provide a URL to a working system
* Only implement one recommender algorithm
* Example [here](https://github.com/wyo9057/movie_recommender_system).

## Marks
1. Incorporate a dataset of books ratings. The dataset should maintain two tables. One
table comprises data of user ID, book ID, and book rating. Another table comprises
data of book ID, book title and book genres. [15]
2. Maintain user profile to store user preference of books. [15]
3. Apply user profile to provide book recommendation based on a suitable
recommendation algorithm. [50]
4. Provide a suitable interface for a user to interact with the system, supporting user profile
creation and/or update and receiving book recommendations

