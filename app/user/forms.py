from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email


class ResetPasswordForm(FlaskForm):
    email = StringField('Email Address', [DataRequired(), Email()])


class LoginForm(ResetPasswordForm):
    password = PasswordField('Password', [DataRequired()])
