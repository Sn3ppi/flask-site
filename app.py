from flask import Flask, render_template, url_for, request, redirect 
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime 


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db' 
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False 
db = SQLAlchemy(app)


class Article(db.Model): 
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False) 
    text = db.Column(db.Text, nullable=False) 
    date = db.Column(db.DateTime, default=datetime.utcnow)  
    def __repr__(self): 
        return '<Article %r>' % self.id 


@app.route('/')
def index():
    return render_template('main_page.html')


@app.route('/create_article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        title = request.form['title'] 
        intro = request.form['intro']
        text = request.form['text']
        article = Article(title=title, intro=intro, text=text) 
        try:
            db.session.add(article) 
            db.session.commit() 
            return redirect('/articles')
        except:
            return "При добавлении статьи произошла ошибка. :("
    else:
        return render_template('create_article.html')


@app.route('/articles')
def short_articles():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('articles.html', articles=articles) 


@app.route('/articles/<int:id>')
def full_article(id):
    article = Article.query.get(id) 
    return render_template("full_article.html", article=article)


@app.route('/articles/<int:id>/del')
def delete_article(id):
    article = Article.query.get_or_404(id) 
    try: 
        db.session.delete(article) 
        db.session.commit() 
        return redirect('/articles') 
    except:
        return "При удалении статьи произошла ошибка. :("


@app.route('/articles/<int:id>/update', methods=['POST', 'GET']) 
def update_article(id):
    if request.method == "POST":
        title = request.form['title'] 
        intro = request.form['intro']
        text = request.form['text']
        article = Article(title=title, intro=intro, text=text) 
        try:
            db.session.add(article)
            db.session.commit() 
            return redirect('/articles') 
        except:
            return "При редактировании статьи произошла ошибка. :("
    else:
        article = Article.query.get(id) 
        return render_template('update_article.html', article=article) 


if __name__ == "__main__":
    app.run(debug=True)






