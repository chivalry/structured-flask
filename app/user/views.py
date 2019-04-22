from flask import (render_template, Blueprint, url_for, redirect, flash, request, current_app,
                   abort)
from flask_login import login_user, logout_user, login_required
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadSignature

from . import LoginForm, ResetPasswordForm, PasswordForm
from .. import mail, bcrypt, User, db
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


@user_blueprint.route('/reset', methods=['GET', 'POST'])
def reset():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.select_by_email(email=email)
        if user:
            timed_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
            token = timed_serializer.dumps(email, salt='recovery-token')
            url = url_for('user.reset_with_token', token=token, _external=True)
            body = render_template('email/recover.txt', url=url)
            html = render_template('email/recover.html', url=url)
            msg = Message(body=body, html=html, recipients=[email],
                          subject=const.RESET_EMAIL_SUBJECT)
            mail.send(msg)
        flash(const.RESET_PASSWORD_REQUEST_FLASH, 'success')
        return redirect(url_for('user.login'))
    return render_template('user/reset.html', form=form)


@user_blueprint.route('/reset/<token>', methods=['GET', 'POST'])
def reset_with_token(token):
    timed_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = timed_serializer.loads(token, salt='recovery-token', max_age=3600)
    except BadSignature:
        abort(404)
    form = PasswordForm()
    if form.validate_on_submit():
        query = User.select_by_email(email=email)
        if query:
            user = query.first()
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
        flash(const.RESET_PASSWORD_SUCCESS, 'success')
        return redirect(url_for('user.login'))
    return render_template('user/password.html', form=form)
