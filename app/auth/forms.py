from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l
from app.models import User


class LoginForm(FlaskForm):

    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))

class RegistrationForm(FlaskForm):

    username = StringField(_l('Username'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password_repeat = PasswordField(_l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Register'))

    def validate_username(self, username):

        user = User.query.filter_by(username=username.data).first()

        if user is not None:

            raise ValidationError(_('That username is already taken. Please use another.'))

    def validate_email(self, email):

        user = User.query.filter_by(email=email.data).first()

        if user is not None:

            raise ValidationError(_('That email address is already taken. Please use another.'))

class DeleteUserForm(FlaskForm):

    submit = SubmitField(_l('Delete user'))