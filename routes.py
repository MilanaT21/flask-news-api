from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, News

app = Blueprint('app', __name__)

@app.route('/')
def index():
    news = News.query.all()
    return render_template('index.html', news=news)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed_password = generate_password_hash(request.form['password'])
        user = User(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            email=request.form['email'],
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Успешная регистрация!')
        return redirect(url_for('app.login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('app.dashboard'))
        flash('Неверный email или пароль')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('app.index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_news = News.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', news=user_news)

@app.route('/news/create', methods=['GET', 'POST'])
@login_required
def create_news():
    if request.method == 'POST':
        news = News(
            title=request.form['title'],
            content=request.form['content'],
            user_id=current_user.id
        )
        db.session.add(news)
        db.session.commit()
        return redirect(url_for('app.dashboard'))
    return render_template('create_news.html')

@app.route('/news/edit/<int:news_id>', methods=['GET', 'POST'])
@login_required
def edit_news(news_id):
    news = News.query.get_or_404(news_id)
    if news.author != current_user:
        flash('Вы не можете редактировать эту новость')
        return redirect(url_for('app.dashboard'))
    if request.method == 'POST':
        news.title = request.form['title']
        news.content = request.form['content']
        db.session.commit()
        return redirect(url_for('app.dashboard'))
    return render_template('edit_news.html', news=news)

@app.route('/news/delete/<int:news_id>')
@login_required
def delete_news(news_id):
    news = News.query.get_or_404(news_id)
    if news.author != current_user:
        flash('Вы не можете удалить эту новость')
        return redirect(url_for('app.dashboard'))
    db.session.delete(news)
    db.session.commit()
    return redirect(url_for('app.dashboard'))
