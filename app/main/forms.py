from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Length, NumberRange
from flask_babel import _, lazy_gettext as _l
from app.models import User, Book


class EditProfileForm(FlaskForm):

    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About me'), validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):

        super(EditProfileForm, self).__init__(*args, **kwargs)

        self.original_username = original_username

    def validate_username(self, username):

        if username.data != self.original_username:

            user = User.query.filter_by(username=self.username.data).first()

            if user is not None:

                raise ValidationError(_('That username is already taken. Please use another.'))


class RateBookForm(FlaskForm):

    title = StringField(_l("Title"), validators=[DataRequired()])
    rating = IntegerField(_l("Please enter a rating"), validators=[DataRequired(), NumberRange(0, 5)])
    submit = SubmitField(_l('Rate'))

    def get_book_id(self):

        return self.book_id

    def validate_title(self, title):

        title = title.data.lower().strip()

        books = [str(book.title).lower().strip() for book in Book.query.all() if book.title is not None]

        i = books.index(title)

        if i == -1:

            raise ValidationError(_("That book is not in the database."))

        self.book_id = i + 1



