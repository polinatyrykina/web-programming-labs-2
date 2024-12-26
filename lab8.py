import os
from flask import Blueprint, render_template, request, redirect, session
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    return render_template('lab8/lab8.html')

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
    return redirect('/lab8/')

@lab8.route('/lab8/login',methods = ['GET','POST'])
def login():
        if request.method == 'GET':
                return render_template('lab8/login.html')
        
        login_form = request.form.get('login')
        password_form = request.form.get('password')

        user = users.query.filter_by(login=login_form).first()

        if not login_form or not password_form:
                return render_template('lab8/register.html', error='Логин и пароль не могут быть пустыми')

        if user:
                if check_password_hash(user.password, password_form):
                        login_user(user, remember = False)
                        return redirect('/lab8/')
        return render_template('lab8/login.html', 
                               error='Ошибка вход: логин и/или пароль неверны')

@lab8.route('/lab8/articles') 
@login_required
def article_list():
        return "список статей" 
        # return render_template('lab8/articles.html')

@lab8.route('/lab8/create') 
def create(): 
        return render_template('lab8/create_article.html')

