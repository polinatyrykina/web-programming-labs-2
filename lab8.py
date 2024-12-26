import os
from flask import Blueprint, render_template, request, redirect, session
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    user_login = current_user.login if current_user.is_authenticated else None
    return render_template('lab8/lab8.html', login=user_login)

@lab8.route('/lab8/register',methods = ['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    # Проверка на пустые значения
    if not login_form or not password_form:
        return render_template('lab8/register.html', error='Логин и пароль не могут быть пустыми')

    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html', error='Такой логин уже существует')
    
    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user, remember=False)
    return redirect('/lab8/')

@lab8.route('/lab8/login',methods = ['GET','POST'])
def login():
        if request.method == 'GET':
                return render_template('lab8/login.html')
        
        login_form = request.form.get('login')
        password_form = request.form.get('password')
        remember = request.form.get('remember') == 'on'

        user = users.query.filter_by(login=login_form).first()

        if not login_form or not password_form:
                return render_template('lab8/register.html', error='Логин и пароль не могут быть пустыми')

        if user:
                if check_password_hash(user.password, password_form):
                        login_user(user, remember = remember)
                        return redirect('/lab8/')
        return render_template('lab8/login.html', 
                               error='Ошибка вход: логин и/или пароль неверны')


@lab8.route('/lab8/logout') 
@login_required
def logout():
        logout_user()
        return redirect('/lab8/')

@lab8.route('/lab8/articles/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'on'

    new_article = articles(
        title=title,
        artcicle_text=article_text,
        login_id=current_user.id,
        is_public=is_public,
        likes=0
    )
    db.session.add(new_article)
    db.session.commit()
    return redirect('/lab8/articles')

@lab8.route('/lab8/articles/<int:article_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.get_or_404(article_id)
    if article.login_id != current_user.id:
        return "У вас нет прав на редактирование этой статьи", 403
    
    if request.method == 'GET':
        return render_template('lab8/edit_article.html', article=article)
    
    article.title = request.form.get('title')
    article.article_text = request.form.get('article_text')
    db.session.commit()
    return redirect('/lab8/articles')

@lab8.route('/lab8/articles/<int:article_id>/delete', methods=['POST']) 
@login_required 
def delete_article(article_id): 
    print(f"Deleting article with ID: {article_id}")  # Логируем ID статьи
    article = articles.query.get_or_404(article_id) 
    if article.login_id != current_user.id: 
        return "У вас нет прав на удаление этой статьи", 403 
       
    db.session.delete(article) 
    db.session.commit() 
    return redirect('/lab8/articles')

@lab8.route('/lab8/articles')
def article_list():
    search_query = request.args.get('search', '').strip() 
    query = articles.query
    if current_user.is_authenticated:
        query = query.filter((articles.login_id == current_user.id) | (articles.is_public == True))
    else:
        query = query.filter(articles.is_public == True)
    if search_query:
        query = query.filter(articles.title.ilike(f'%{search_query}%') | articles.artcicle_text.ilike(f'%{search_query}%'))
    all_articles = query.all()

    articles_with_authors = []
    for article in all_articles:
        author = users.query.get(article.login_id) 
        articles_with_authors.append((article, author))

    return render_template('lab8/articles.html', articles=articles_with_authors, search_query=search_query)
