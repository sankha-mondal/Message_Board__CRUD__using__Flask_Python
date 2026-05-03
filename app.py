from flask import Flask, render_template, request, redirect, url_for
from models import db, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    posts = Post.query.filter_by(is_published=True).all()
    return render_template('index.html', posts=posts)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        is_published = 'publish' in request.form

        post = Post(title=title, content=content, is_published=is_published)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = Post.query.get_or_404(id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.is_published = 'publish' in request.form

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    total = Post.query.count()
    published = Post.query.filter_by(is_published=True).count()
    drafts = total - published

    return render_template('dashboard.html',
                           total=total,
                           published=published,
                           drafts=drafts)

if __name__ == '__main__':
    app.run(debug=True)
