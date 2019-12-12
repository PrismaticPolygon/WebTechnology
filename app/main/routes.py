from datetime import datetime
from flask import render_template, redirect, url_for, request, g, jsonify
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from app import db
from app.main.forms import RateBookForm
from app.models import User, Book, Rating
from app.main import bp


@bp.before_app_request
def before_request():

    if current_user.is_authenticated:

        current_user.last_seen = datetime.utcnow()
        db.session.commit()

    g.locale = str(get_locale())

@bp.route('/')
@bp.route('/index')
def index():

    books = Book.query.all()

    return render_template('index.html', title=_('Home'), books=books)


@bp.route('/user/<username>', methods=["GET", "POST"])
@login_required
def user(username):

    user = User.query.filter_by(username=username).first_or_404()
    form = RateBookForm()

    if form.validate_on_submit():

        user_id = current_user.id
        book_id = form.book_id

        rating = Rating.query.filter_by(book_id=book_id, user_id=user_id).first()

        if rating is None:

            rating = Rating(book_id=book_id, user_id=user_id, value=form.rating.data)

            db.session.add(rating)

        else:

            rating.value = form.rating.data

        db.session.commit()

        return redirect(url_for('main.user', username=user.username))

    ratings = user.get_ratings()
    recommendations = user.get_recommendations()

    return render_template('user.html',
                           user=user,
                           ratings=ratings,
                           recommendations=recommendations,
                           form=form)