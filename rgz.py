from flask import Flask, render_template, request, redirect, url_for, session, flash, current_app,Blueprint
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

rgz = Blueprint('rgz',__name__)

# Функции для работы с БД
def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='rgz-web',
            user='polina_tyrykina_knowledge_base',
            password='123',
            port=5432
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

# Маршруты
@rgz.route('/rgz/')
@rgz.route('/rgz/index')
def index():
    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM userss WHERE is_hidden = FALSE")  # Получаем только видимые анкеты
    else:
        cur.execute("SELECT * FROM userss WHERE is_hidden = FALSE") 

    users = cur.fetchall()
    db_close(conn, cur)
    return render_template('rgz/index.html', users=users)

@rgz.route('/rgz/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        service_type = request.form['service_type']
        experience = int(request.form['experience'])
        price = int(request.form['price'])
        about = request.form['about']

        # Проверка, существует ли пользователь с таким именем
        conn, cur = db_connect()
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM userss WHERE username = %s", (username,))
        else:
            cur.execute("SELECT * FROM userss WHERE username = ?", (username,))
        existing_user = cur.fetchone()
        db_close(conn, cur)

        if existing_user:
            flash('Пользователь с таким именем уже существует')
            return redirect(url_for('rgz.register'))

        # Если пользователь не существует, выполняем вставку
        conn, cur = db_connect()
        cur.execute("INSERT INTO userss (username, password, name, service_type, experience, price, about) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (username, password, name, service_type, experience, price, about))
        db_close(conn, cur)
        flash('Регистрация прошла успешно')
        return redirect(url_for('rgz.login'))

    return render_template('rgz/register.html')

@rgz.route('/rgz/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn, cur = db_connect()
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM userss WHERE username = %s AND password = %s", (username, password))
        else:
            cur.execute("SELECT * FROM userss WHERE username = ? AND password = ?", (username, password))
        user = cur.fetchone()
        db_close(conn, cur)

        if user:
            session['user_id'] = user['id']
            session['is_admin'] = user['is_admin']
            return redirect('/rgz/profile')
        
        else:
            flash('Неверный логин или пароль')
    return render_template('rgz/login.html')

@rgz.route('/rgz/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect('/rgz/login')

    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM userss WHERE id = %s", (session['user_id'],))
    else:
        cur.execute("SELECT * FROM userss WHERE id = ?", (session['user_id'],))
    user = cur.fetchone()
    db_close(conn, cur)

    if request.method == 'POST':
        name = request.form['name']
        service_type = request.form['service_type']
        experience = int(request.form['experience'])
        price = int(request.form['price'])
        about = request.form['about']
        is_hidden = 'is_hidden' in request.form

        conn, cur = db_connect()
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE userss SET name = %s, service_type = %s, experience = %s, price = %s, about = %s, is_hidden = %s WHERE id = %s",
                        (name, service_type, experience, price, about, is_hidden, session['user_id']))
        else:
            cur.execute("UPDATE userss SET name = ?, service_type = ?, experience = ?, price = ?, about = ?, is_hidden = ? WHERE id = ?",
                        (name, service_type, experience, price, about, is_hidden, session['user_id']))
        db_close(conn, cur)
        return redirect('/rgz/profile')

    return render_template('/rgz/profile.html', user=user)

@rgz.route('/rgz/search', methods=['GET'])
def search():
    query = request.args.get('query')
    service_type = request.args.get('service_type')
    min_experience = request.args.get('min_experience')
    max_experience = request.args.get('max_experience')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    page = int(request.args.get('page', 1))

    # Начальный запрос
    sql = "SELECT * FROM userss WHERE is_hidden = FALSE"
    params = []

    # Добавляем условия в запрос, если значения заданы
    if query:
        sql += " AND name LIKE %s"
        params.append(f"%{query}%")

    if service_type:
        sql += " AND service_type = %s"
        params.append(service_type)

    if min_experience:
        sql += " AND experience >= %s"
        params.append(min_experience)

    if max_experience:
        sql += " AND experience <= %s"
        params.append(max_experience)

    if min_price:
        sql += " AND price >= %s"
        params.append(min_price)

    if max_price:
        sql += " AND price <= %s"
        params.append(max_price)

    # Добавляем пагинацию
    sql += " LIMIT 5 OFFSET %s"
    params.append((page - 1) * 5)

    # Выполняем запрос
    conn, cur = db_connect()
    cur.execute(sql, params)
    results = cur.fetchall()
    db_close(conn, cur)

    return render_template('/rgz/search.html', results=results, page=page)


@rgz.route('/rgz/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/rgz/index')

@rgz.route('/rgz/delete_account')
def delete_account():
    if 'user_id' not in session:
        return redirect('/rgz/login')

    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM userss WHERE id = %s", (session['user_id'],))
    else:
        cur.execute("DELETE FROM userss WHERE id = ?", (session['user_id'],))
    db_close(conn, cur)
    session.pop('user_id', None)
    return redirect('/rgz/index')

@rgz.route('/rgz/admin')
def admin():
    if 'user_id' not in session:
        return redirect('rgz/login')

    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM userss WHERE is_admin = TRUE AND id = %s", (session['user_id'],))
    else:
        cur.execute("SELECT * FROM userss WHERE is_admin = TRUE AND id = ?", (session['user_id'],))
    admin_user = cur.fetchone()
    db_close(conn, cur)

    if not admin_user:
        return redirect('/rgz/index')

    conn, cur = db_connect()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    db_close(conn, cur)

    return render_template('/rgz/admin.html', users=users)

@rgz.route('/rgz/user/<int:user_id>')
def user_profile(user_id):
    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM userss WHERE id = %s", (user_id,))
    else:
        cur.execute("SELECT * FROM userss WHERE id = ?", (user_id,))
    user = cur.fetchone()
    db_close(conn, cur)

    if not user:
        flash('Анкета не найдена')
        return redirect('/rgz/index')

    return render_template('/rgz/user_profile.html', user=user)


@rgz.route('/rgz/admin/users')
def admin_users():
    if 'user_id' not in session:
        return redirect(url_for('rgz.login'))

    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM userss WHERE id = %s", (session['user_id'],))
    else:
        cur.execute("SELECT * FROM userss WHERE id = ?", (session['user_id'],))
    user = cur.fetchone()
    db_close(conn, cur)

    if not user or not user['is_admin']:
        flash('У вас нет доступа к этой странице')
        return redirect(url_for('rgz.index'))

    conn, cur = db_connect()
    cur.execute("SELECT * FROM userss")
    users = cur.fetchall()
    db_close(conn, cur)

    return render_template('rgz/admin_users.html', users=users)


@rgz.route('/rgz/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
def admin_edit_user(user_id):
    if 'user_id' not in session:
        return redirect(url_for('rgz.login'))

    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM userss WHERE id = %s", (session['user_id'],))
    else:
        cur.execute("SELECT * FROM userss WHERE id = ?", (session['user_id'],))
    admin_user = cur.fetchone()
    db_close(conn, cur)

    if not admin_user or not admin_user['is_admin']:
        flash('У вас нет доступа к этой странице')
        return redirect(url_for('rgz.index'))

    if request.method == 'POST':
        name = request.form['name']
        service_type = request.form['service_type']
        experience = int(request.form['experience'])
        price = int(request.form['price'])
        about = request.form['about']
        is_hidden = 'is_hidden' in request.form

        conn, cur = db_connect()
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                UPDATE userss
                SET name = %s, service_type = %s, experience = %s, price = %s, about = %s, is_hidden = %s
                WHERE id = %s
            """, (name, service_type, experience, price, about, is_hidden, user_id))
        else:
            cur.execute("""
                UPDATE userss
                SET name = ?, service_type = ?, experience = ?, price = ?, about = ?, is_hidden = ?
                WHERE id = ?
            """, (name, service_type, experience, price, about, is_hidden, user_id))
        db_close(conn, cur)
        flash('Пользователь успешно отредактирован')
        return redirect(url_for('rgz.admin_users'))

    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM userss WHERE id = %s", (user_id,))
    else:
        cur.execute("SELECT * FROM userss WHERE id = ?", (user_id,))
    user = cur.fetchone()
    db_close(conn, cur)

    return render_template('rgz/admin_edit_user.html', user=user)



@rgz.route('/rgz/admin/delete_user/<int:user_id>')
def admin_delete_user(user_id):
    if 'user_id' not in session:
        return redirect(url_for('rgz.login'))

    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM userss WHERE id = %s", (session['user_id'],))
    else:
        cur.execute("SELECT * FROM userss WHERE id = ?", (session['user_id'],))