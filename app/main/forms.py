from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, NumberRange
from flask_babel import _, lazy_gettext as _l
from app.models import Book, Rating

class RateBookForm(FlaskForm):

    title = StringField(_l("Title or ID"), validators=[DataRequired()])
    rating = IntegerField(_l("Please enter a rating"), validators=[DataRequired(), NumberRange(0, 5)])
    submit = SubmitField(_l('Rate'))

    def validate_title(self, title):

        title = title.data.lower().strip()

        try:

            book_id = int(title)

        except ValueError:

            books = [str(book.title).lower().strip() for book in Book.query.all() if book.title is not None]

            book_id = books.index(title) + 1

        if book_id == 0:

            raise ValidationError(_("That book is not in the database."))

        self.book_id = book_id

class DeleteRatingForm(FlaskForm):

    # We have to check whether the rating exists.

    title = StringField(_l("Title or ID"), validators=[DataRequired()])
    submit = SubmitField(_l('Delete'))

    def validate_title(self, title):

        title = title.data.lower().strip()

        try:

            book_id = int(title)

        except ValueError:

            books = [str(book.title).lower().strip() for book in Book.query.all() if book.title is not None]

            book_id = books.index(title) + 1

        if book_id == 0:

            raise ValidationError(_("That book is not in the database."))

        rating = Rating.query.filter_by(book_id=book_id, user_id=self.user_id).first()

        if rating is None:

            raise ValidationError(_("You have not rated this book."))

        self.rating_id = rating.id
        self.book_id = book_id

    def set_user_id(self, user_id):

        self.user_id = user_id



