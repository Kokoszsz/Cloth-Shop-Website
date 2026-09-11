from flask import Blueprint, redirect, render_template, request, session, url_for
from flask.typing import ResponseReturnValue

from blueprints import db_Session
from database import create_user, get_users, update_user
from exceptions import DuplicateUser
from utils import ValidationError, authenticate, validate_account

bp = Blueprint('auth', __name__)


def messages_by_field(errors: list[ValidationError]) -> dict[str, str]:
    return {error.field: error.message for error in errors}


@bp.route('/account', methods = ['POST', 'GET'])
def account() -> ResponseReturnValue:
    errors: list[ValidationError] = []

    if 'user' not in session:
        return redirect(url_for('auth.login'))
    else:
        if request.method == 'POST':

            id = session['user']['id']
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            surname = request.form['surname']
            phone_number = request.form['phone']
            country = request.form['country']
            city = request.form['city']

            users = get_users(db_Session())

            errors = validate_account(users, id, username, email, password)
            if not errors:
                user = update_user(
                    db_Session(), id, username, password, email, users,
                    surname, phone_number, country, city,
                )
                session['user'] = user.to_dict()

        user_info = session['user']
        return render_template(
            'account.html', user_info = user_info, errors = messages_by_field(errors)
        )

@bp.route('/login', methods = ['POST', 'GET'])
def login() -> ResponseReturnValue:
    error = None
    if request.method == 'POST':

        if request.form['action'] == "Create account":
            return redirect(url_for('auth.create_account'))

        username = request.form['login']
        password = request.form['password']

        users = get_users(db_Session())
        user_info, error = authenticate(username, password, users)

        if user_info is not None:
            session['user'] = user_info.to_dict()
            return redirect(url_for('auth.account'))

    return render_template('login.html', error = error.message if error else None)


@bp.route('/create_account', methods = ['POST', 'GET'])
def create_account() -> ResponseReturnValue:

    errors: list[ValidationError] = []

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        users = get_users(db_Session())

        errors = validate_account(users, None, username, email, password)

        if not errors:
            try:
                user = create_user(db_Session(), username, password, email)
            except DuplicateUser:
                errors = [ValidationError('username', 'Already such an User')]
            else:
                session['user'] = user.to_dict()
                return redirect(url_for('auth.account'))

    return render_template('create_account.html', errors = messages_by_field(errors))


@bp.route('/logout')
def logout() -> ResponseReturnValue | None:
    if 'user' in session:
        session.pop('user', None)
        session['basket'] = []
        return redirect(url_for('catalogue.home'))
    else:
        pass
