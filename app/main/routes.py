from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from app import db
from app.main.forms import EditProfileForm, SearchForm
from app.models import User, Post
from app.translate import translate
from app.main import bp


@bp.before_app_request
def before_request():

    if current_user.is_authenticated:

        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()

    g.locale = str(get_locale())

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():

    return render_template('index.html', title=_('Home'))


@bp.route('/user/<username>')
@login_required
def user(username):

    user = User.query.filter_by(username=username).first_or_404()

    # page = request.args.get('page', 1, type=int)

    return render_template('user.html', user=user)


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

@bp.route('/search')
def search():

    if not g.search_form.validate():

        return redirect(url_for('main.index'))

    page = request.args.get('page', 1, type=int)

    posts, total = Post.search(g.search_form.q.data, page, current_app.config['POSTS_PER_PAGE'])

    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) if page > 1 else None

    return render_template('search.html',
                           title=_('Search'),
                           posts=posts,
                           next_url=next_url,
                           prev_url=prev_url)