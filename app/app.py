from os import path
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

DB_NAME = 'blog.db'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db = SQLAlchemy(app)


class PostToBlog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(50))
    datetime = db.Column(db.DateTime)
    content = db.Column(db.Text)


@app.route('/')
def index():
    posts = PostToBlog.query.order_by(PostToBlog.datetime.desc()).all()
    return render_template('index.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/add')
def add():
    return render_template('add.html')


@app.route('/addpost', methods=['POST'])
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']

    new_post = PostToBlog(title=title, subtitle=subtitle, author=author, content=content, datetime=datetime.now())

    db.session.add(new_post)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/post/<int:post_id>', methods=['GET', 'DELETE'])
def post(post_id):
    post = PostToBlog.query.filter_by(id=post_id).one()
    return render_template('post.html', post=post)


@app.route("/delete/<int:post_id>")
def delete(post_id):
    post = PostToBlog.query.filter_by(id=post_id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')


if __name__ == '__main__':
    create_database(app)
    app.run(debug=True)
