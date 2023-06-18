from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db=SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>'%self.id

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', articles=articles)

@app.route('/post/<int:id>')
def posts_detail(id):
    article = Article.query.get(id)
    return render_template('post_detail.html', article=article)

@app.route('/post/<int:id>/delete')
def post_delete(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "Error while deleting :("


@app.route('/post/<int:id>/edit', methods = ['POST','GET'])
def update_article(id):
    if request.method == "POST":
        article=Article.query.get(id)
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return 'Error while adding article'
    else:
        article=Article.query.get(id)
        return render_template('update_article.html', article=article)

@app.route('/create_article', methods = ['POST','GET'])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        article=Article(title=title, intro=intro,text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return 'Error while adding article'
    else:
        return render_template('create_article.html')

@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return "user page" + name + '-' + str(id)

@app.route('/order')
def order():
    return "This is order page"

if __name__ == '__main__':
    app.run(debug=True)
