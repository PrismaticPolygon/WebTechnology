from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from app import db
from app.main.forms import EditProfileForm
from app.models import User, Book
from app.translate import translate
from app.main import bp


@bp.before_app_request
def before_request():

    if current_user.is_authenticated:

        current_user.last_seen = datetime.utcnow()
        db.session.commit()

    g.locale = str(get_locale())

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():

    books = Book.query.all()

    return render_template('index.html', title=_('Home'), books=books)


@bp.route('/user/<username>')
@login_required
def user(username):

    user = User.query.filter_by(username=username).first_or_404()

    ratings = user.get_ratings()
    recommendations = user.get_recommendations()

    return render_template('user.html', user=user, ratings=ratings, recommendations=recommendations)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():

    form = EditProfileForm(current_user.username)

    if form.validate_on_submit():

        current_user.username = form.username.data
        current_user.about_me = form.about_me.data

        db.session.commit()

        flash(_('Your changes have been saved.'))

        return redirect(url_for('main.edit_profile'))

    elif request.method == 'GET':

        form.username.data = current_user.username

        form.about_me.data = current_user.about_me

    return render_template('edit_profile.html', title=_('Edit Profile'), form=form)


@bp.route('/translate', methods=['POST'])
@login_required
def translate_text():

    return jsonify({'text': translate(request.form['text'],
                                      request.form['source_language'],
                                      request.form['dest_language'])})