from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email


class ResetPasswordForm(FlaskForm):
    email = StringField('Email Address', [DataRequired(), Email()])


class PasswordForm(FlaskForm):
    password = PasswordField('Password', [DataRequired()])


class LoginForm(FlaskForm):
    email = StringField('Email Address', [DataRequired(), Email()])
    password = PasswordField('Password', [DataRequired()])
