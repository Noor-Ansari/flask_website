from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SECRET_KEY']  = '786941674jrhgiwjegri982346923'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(20), nullable=False, default = 'N/A')
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return "Blog Post :-" + str(self.id)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method=='POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        new_post = BlogPost(title=title, content=content, author=author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.all()
        return render_template('posts.html', posts=all_posts)

@app.route('/posts/delete/<int:id>')
def delete(id):
    post_to_delete = BlogPost.query.get(id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post_to_edit = BlogPost.query.get(id)
    if request.method=='POST':
        post_to_edit.title = request.form['title']
        post_to_edit.content = request.form['content']
        post_to_edit.author = request.form['author']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', posts=post_to_edit)

@app.route('/posts/new', methods=['GET', 'POST'])
def new_posts():
    if request.method=='POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        new_post = BlogPost(title=title, content=content, author=author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template("new_post.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account has been created for {form.username.data}', 'success')
        return redirect(url_for('posts'))
    return render_template('register.html', form=form)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


if (__name__)=='__main__':
    app.run(debug=True)
