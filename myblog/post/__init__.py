import os
import sqlite3
import click
import sys
from flask import Flask,render_template,request,g,current_app,redirect, url_for, flash
from flask.cli import with_appcontext
from datetime import datetime, date

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'blog.sqlite'),
    )

@app.route('/')
def render():
    return render_template('index.html')


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def get_post(id):
    post = get_db().execute(
        "select * from post p where p.id = ?",
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    return post

def get_all_post():
    post = get_db().execute(
        "select id,title, body from post"
    ).fetchall()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    return post


@app.route('/create', methods=['GET','POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        created = request.form['created']
        tags = request.form['tags']
        error = None
        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body,created)'
                ' VALUES (?, ?, ?)',
                (title, body, created)
            )
            db.commit()
            return 'Post created successsfully!!'

    return render_template('create.html')


@app.route('/update', methods=['GET','POST'])
def show_post():
    posts = get_all_post()
    return render_template('show_post.html',posts=posts)

@app.route('/delete', methods=['GET','POST'])
def show_post_delete():
    posts = get_all_post()
    return render_template('show_post_delete.html',posts=posts)


@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    posts = get_post(id)
    if request.method == 'POST':
        title = request.form.get('title', False)
        body = request.form.get('body',False)
        # created = request.form
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('show_post'))
    return render_template('update.html',posts=posts)


@app.route('/delete/<int:id>',methods=['POST'])
def delete(id):
    posts = get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE ID =?', (id,))
    db.commit()
    return redirect(url_for('show_post_delete'))