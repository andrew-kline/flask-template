import email
from tokenize import String
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    EmailField,
    PasswordField,
    BooleanField,
)
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField(u"Email", validators=[DataRequired()])
    name = StringField(u"Name")
    password = PasswordField(u"Password", validators=[DataRequired()])
    remember = BooleanField(u"Remember Me", default=False)
