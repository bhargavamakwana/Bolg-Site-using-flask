from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from blog.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    db = get_db()
    posts = db.execute(
        "select id,title,created body from post"
    ).fetchmany(size=5)
    return render_template('index.html',posts=posts)


@bp.route('/index/post?=<int:id>/',methods=('GET', 'POST'))
def full_post(id):
	db = get_db()
	posts = db.execute(
		"select title, body,created from post where id = ?",
		(id,)
		)
	if posts is None:
		abort(404, "Post doesn't exist.".format(id))
	return render_template('article.html',posts=posts)	



@bp.route('/archive')
def archive():
    db = get_db()
    posts = db.execute(
        "select id,title,body,created from post"
    ).fetchall()
    return render_template('article.html',posts=posts)



    