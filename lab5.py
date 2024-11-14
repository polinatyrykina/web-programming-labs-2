from flask import Blueprint, redirect, render_template, request, make_response, redirect, session
import psycopg2
from  psycopg2.extras import RealDictCursor

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login = session.get('login'))

@lab5.route('/lab5/register', methods = ['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password ')

    if not (login or password):
        return render_template('lab5/register.html', error='Заполните все поля')
    
    conn = psycopg2.connect(
        host = '127.0.0.1',
        database = 'polina_tyrykina_knowledge_base',
        user = 'polina_tyrykina_knowledge_base',
        password = '123'
    )

    cur = conn.cursor()

    cur.execute(f"SELECT login FROM users WHERE login='{login}';")
    if cur.fetchone():
        cur.close()
        conn.close()
        return render_template('lab5/register.html',
                               error = "Такой пользователь не существует")
    
    cur.execute(f"INSERT INTO users (login,password) VALUES ('{login}', '{password}');")
    conn.commit()
    cur.close()
    conn.close()
    return render_template('lab5/success.html', login=login)

@lab5.route('/lab5/success')
def success():
    login = request.args.get('login')
    return render_template('lab5/success.html', login=login)


@lab5.route('/lab5/login', methods=['GET','POST']) 
def login(): 
    if request.method == 'GET': 
        return render_template('lab5/login.html') 
     
    login = request.form.get('login') 
    password = request.form.get('password')  # Убрали лишний пробел
 
    if not (login and password):  # Исправлено на "and"
        return render_template('lab5/login.html', error='Заполните все поля') 
     
    conn = psycopg2.connect( 
        host='127.0.0.1', 
        database='polina_tyrykina_knowledge_base', 
        user='polina_tyrykina_knowledge_base', 
        password='123' 
    ) 
 
    cur = conn.cursor(cursor_factory=RealDictCursor) 
 
    cur.execute("SELECT * FROM users WHERE login=%s;", (login,)) 
    user = cur.fetchone() 

    if not user: 
        cur.close() 
        conn.close() 
        return render_template('lab5/login.html', error='Логин и/или пароль неверны') 

    if user['password'] != password:  
        cur.close() 
        conn.close() 
        return render_template('lab5/login.html', error='Логин и/или пароль неверны') 

    session['login'] = login 
    cur.close() 
    conn.close() 
    return render_template('lab5/success_login.html', login=login)
    