from flask import render_template, Blueprint, url_for, redirect, flash, request
from flask_login import login_user, logout_user, login_required

from .. import bcrypt
from ..models import User
from .forms import LoginForm
from .. import constants as const

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            login_user(user)
            flash(const.LOGIN_SUCCESS_MSG, 'success')
            return redirect(url_for('main.home'))
        else:
            flash(const.LOGIN_FAILURE_MSG, 'danger')
            return render_template('user/login.html', form=form)
    return render_template('user/login.html', title='Please Login', form=form)


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash(const.LOGOUT_SUCCESS_MSG, 'success')
    return redirect(url_for('main.home'))
