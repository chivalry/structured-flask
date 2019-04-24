"""Constants that need to be referenced from various modules."""
from flask_babel import lazy_gettext as _l
from flask_babel import _

LOGIN_SUCCESS_MSG = _('You are logged in. Welcome!')
LOGIN_FAILURE_MSG = _('Invalid email or password.')
LOGIN_DIRECTIVE_MSG = _('Please log in to access this page.')
LOGOUT_SUCCESS_MSG = _('You were logged out. Bye!')

RESET_EMAIL_SUBJECT = _('Password reset requested')
RESET_PASSWORD_REQUEST_FLASH = _('Please check your email.')
RESET_PASSWORD_SUCCESS = _('Your password has been saved.')

FORM_LABEL_EMAIL_ADDRESS = _l('Email Address')
FORM_LABEL_PASSWORD = _l('Password')
FORM_LABEL_CONFIRM_PASSWORD = _l('Confirm Password')
