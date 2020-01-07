# Web Technology

This coursework is based on [this](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) 
tutorial. It is hosted on [Heroku](https://ffgt86-web-technology.herokuapp.com/).

### Users

There are `n=50` users in the system; this can be programmatically set in `generate.py`. Each user has a username of the
 form `user_i`, where `i` is in the range `[1, n]`.
Each password follows the same format, i.e.`password_i`. Passwords are hashed using MD5.
User tokens are stored in cookies; sessions persist.
Users can be created by clicking `Register`. A unique id and email must be specified. Users can delete their profiles 
on the profile page. URLs are appropriately guarded; an unauthenticated user will not be able to access the profile
of a different user. 

### Ratings

Ratings are quasi-randomly generated in `generate.py`. 
Each user is given genre preferences, and between `10 - 50` ratings are calculated
using these preferences as weights. Ratings can be created, updated, and deleted on the user page. 
If a user has no ratings, a random sample of books is recommended.

### Books

Book data is taken from [Goodreads](https://www.goodreads.com/choiceawards/best-books-2019?int=gca_signed_out_hp),
and was entered manually by hand. Considerable effort was expended using the dataset [here](https://github.com/zygmuntz/goodbooks-10k),
but parsing tags proved too unreliable. There are `100` books in the database comprising `41` distinct genres. 

### Recommendations

Recommendations are generated using the tutorial [here](https://beckernick.github.io/matrix-factorization-recommender/),
with some tweaks. 

### Localisation / i18n

The website is available in both English and German. Translation is handled by `Babel`. Translations could easily
be extended to the books themselves or other languages. 

### Running locally.

This should prove unnecessary. The system has been tested with Python 3.6. If running locally is necessary,
run the following commands:
* `pip install -r requirements.txt`
* `flask db init`
* `flask db upgrade`
* `flask translate init`
* `flask translate compile`

Finally, to launch the site, run `flask run`, and navigate to `127.0.0.1/5000`.