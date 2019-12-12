from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, NumberRange
from flask_babel import _, lazy_gettext as _l
from app.models import Book

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



