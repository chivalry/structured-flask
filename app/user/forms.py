from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_babel import lazy_gettext as _l

from .. import constants as const


class ResetPasswordForm(FlaskForm):
    email = StringField(const.FORM_LABEL_EMAIL_ADDRESS, [DataRequired(), Email()])


class PasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), [DataRequired()])
    confirm_password = PasswordField(_l('Confirm Password'), [DataRequired(), EqualTo('password')])


class LoginForm(FlaskForm):
    email = StringField(_l('Email Address'), [DataRequired(), Email()])
    password = PasswordField(_l('Password'), [DataRequired()])
