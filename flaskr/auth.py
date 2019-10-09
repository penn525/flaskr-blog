"""
authorization page, inclde:
blueprint, register, login
"""
import functools

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.database import db_session
from flaskr.db import get_db
from flaskr.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """ user register """
    # 1. check username and password
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        # check if username is empty
        if not username:
            error = 'Username is required!'
        # check if password is empty
        elif not password:
            error = 'Password is required!'
        # check if username exists in database
        # mysql 数据库
        elif User.query.filter(User.username == username).first() is not None:
            error = f'User {username} is registered!'
        # sqllite3 数据库
        # elif db.execute(
        #         'SELECT id FROM user WHERE username = ?', (username, )
        #     ).fetchone() is not None:
        #     error = f'User {username} is registered!'
        
        # everthing is allright, reigster user into database
        if error is None:
            db_session.add(User(username, generate_password_hash(password)))
            db_session.commit()

            # db.execute(
            #     'INSERT INTO user (username, password) VALUES (?, ?)',
            #     (username, generate_password_hash(password)) 
            # )
            # db.commit()
            return redirect(url_for('auth.login'))
        
        flash(error)
    
    return render_template('auth/register.html')



@bp.route('/login', methods=['GET', 'POST'])
def login():
    """ user login method """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        # mysql 数据库
        user = User.query.filter(User.username == username).first()

        # sqlite3 数据库
        # user = db.execute(
        #     'SELECT id, username, password FROM user WHERE username = ?',
        #     (username, )
        # ).fetchone()

        if user is None:
            error = 'Incorrect username!'
        # elif not check_password_hash(user['password'], password):
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password!'
        
        if error is None:
            session.clear()
            # session['user_id'] = user['id']
            session['user_id'] = user.id
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    """ user logout """
    session.clear()
    return redirect(url_for('index'))


@bp.before_app_request
def load_logged_in_user():
    """ store logged in user to g object, so it aviliable on subsequent request """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        # mysql数据库
        g.user = User.query.get(user_id)

        # sqlite3 数据库
        # g.user = get_db().execute(
        #     'SELECT id, username, password FROM user WHERE id = ?',
        #     (user_id,)
        # ).fetchone()


def login_required(view):
    """ login decorator """
    # functools.wraps() can update the wrapped function's __doc__, __name__ etc. just like the original function
    @functools.wraps(view)
    def wrapperd_view(**kwargs):
        # print(g.user)
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapperd_view
