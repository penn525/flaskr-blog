import functools

from flask import (Blueprint, Flask, abort, flash, g, redirect,
                   render_template, request, url_for)
from flask_wtf import CSRFProtect

from flaskr.auth import login_required
from flaskr.database import db_session
from flaskr.db import get_db
from flaskr.models import Post, User

bp = Blueprint('blog', __name__) 
csrf = CSRFProtect()


@csrf.exempt # 排除csrf保护
@bp.route('/')
@login_required
def index():
    """ index page, show all posts """
    posts = Post.query.filter(Post.author_id == g.user.id)

    # db = get_db()
    # posts = db.execute(
    #     'SELECT p.id,author_id,title,body,created,username'
    #     ' FROM post p JOIN user u ON p.author_id = u.id'
    #     ' ORDER BY created DESC'
    # ).fetchall()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            # mysql
            post = Post(title, body, g.user.id)
            db_session.add(post)
            db_session.commit()

            # sqlite3
            # db = get_db()
            # db.execute(
            #     'INSERT INTO post (title, body, author_id)'
            #     ' VALUES (?, ?, ?)',
            #     (title, body, g.user['id'])
            # )
            # db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(id, check_author=True):
    """ get a post by a post id and before get_post, we should check if the logged author is the post's author_id """
    # mysql
    post = Post.query.get(id)

    # sqlite3
    # post = get_db().execute(
    #     'SELECT p.id, title, body, created, author_id, username'
    #     ' FROM post p JOIN user u ON p.author_id = u.id'
    #     ' WHERE p.id = ?',
    #     (id, )
    # ).fetchone()

    # no such post
    if post is None:
        abort(404, f'Post id {id} does not exist.')
    # mysql
    if check_author and post.author_id != g.user.id:
        abort(403)
    
    # the post doesnot belong to the logged user
    # if check_author and post['author_id'] != g.user['id']:
    #     abort(403)
    
    return post


@bp.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    """ update a post """
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        
        if not title:
            error = 'Title is required!'
        
        if error is not None:
            flash(error)
        else:
            # mysql
            post = Post.query.get(id)
            post.title = title
            post.body = body
            db_session.commit()

            # sqlite3
            # db = get_db()
            # db.execute(
            #     'UPDATE post SET title = ?, body = ? WHERE id = ?',
            #     (title, body, id)
            # )
            # db.commit()
            return redirect(url_for('blog.index'))


    return render_template('blog/update.html', post=post)


@bp.route('/delete/<int:id>', methods=['POST',])
@login_required
def delete(id):
    """ delete a post """
    get_post(id)
    # mysql
    post = Post.query.get(id)
    db_session.delete(post)
    db_session.commit()

    # sqlite3
    # db = get_db()
    # db.execute('DELETE FROM post WHERE id = ?', (id, ))
    # db.commit()
    return redirect(url_for('index'))
