from flask import Blueprint, url_for, render_template, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
import datetime

from leadliner import db
from leadliner.forms import SignUpForm
from leadliner.forms import UserLoginForm
from leadliner.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup', methods=('GET', 'POST'))
def signup():
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data,
                        join_date=datetime.datetime.now())
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            return redirect(url_for('onboarding.keywords_select'))
        else:
            flash('이미 존재하는 계정입니다.')
    return render_template('signup.html', form=form)


@bp.route('/policy', methods=('GET', 'POST'))
def signup_policy():
    return render_template('policy.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main.home'))
        flash(error)
    return render_template('login.html', form=form)