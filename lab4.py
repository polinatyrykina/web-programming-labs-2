from flask import Blueprint, redirect, render_template, request, make_response, redirect, session
lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form')
def div_form():
    return render_template('/lab4/div-form.html')

@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1') 
    x2 = request.form.get('x2') 
    
    if x1 == '' or x2 == '': 
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!') 
    if x2 == '0': 
        return render_template('lab4/div.html', error1='Делить на 0 нельзя!') 
    
    x1 = int(x1) 
    x2 = int(x2) 
    result = x1 / x2 
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('/lab4/sum-form.html')

@lab4.route('/lab4/sum', methods=['POST'])
def sum_function():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    # Преобразуем в 0, если поля пустые
    x1 = int(x1) if x1 else 0
    x2 = int(x2) if x2 else 0
    
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('/lab4/mul-form.html')

@lab4.route('/lab4/mul', methods=['POST'])
def mul_function():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    # Преобразуем в 1, если поля пустые
    x1 = int(x1) if x1 else 1
    x2 = int(x2) if x2 else 1

    result = x1 * x2
    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('/lab4/sub-form.html')

@lab4.route('/lab4/sub', methods=['POST'])
def sub_function():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)
    
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('/lab4/pow-form.html')

@lab4.route('/lab4/pow', methods=['POST'])
def pow_function():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)

    if x1 == 0 and x2 == 0:
        return render_template('lab4/pow.html', error1='Невозможно возвести 0 в 0.')
    
    result = x1 ** x2
    return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)

tree_count = 0

@lab4.route('/lab4/tree', methods = ['GET','POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)
    
    operation = request.form.get('operation')

    if operation == 'cut': 
        if tree_count > 0:  
            tree_count -= 1 
    elif operation == 'plant': 
        if tree_count < 10:  #
            tree_count += 1 
    return redirect('/lab4/tree')

users = [
    {'login': 'alex', 'password': 'password123', 'name': 'Александр Александров'},
    {'login': 'john9977', 'password': 'abc123', 'name': 'Иван Иванов'},
    # добавьте других пользователей по аналогии...
]

@lab4.route('/lab4/login', methods=['GET', 'POST']) 
def login(): 
    if request.method == 'GET': 
        if 'login' in session: 
            authorized = True 
            login = session['login'] 
            user_name = [user['name'] for user in users if user['login'] == login][0] 
        else: 
            authorized = False 
            login = '' 
            user_name = ''
        return render_template('lab4/login.html', authorized=authorized, login=login, user_name=user_name) 

    login = request.form.get('login') 
    password = request.form.get('password') 

    if not login:
        error = 'Не введён логин'
        return render_template('lab4/login.html', error=error, authorized=False, login=login)

    if not password:
        error = 'Не введён пароль'
        return render_template('lab4/login.html', error=error, authorized=False, login=login)

    for user in users: 
        if login == user['login'] and password == user['password']: 
            session['login'] = login 
            return redirect('/lab4/login') 

    error = 'Неверные логин и/или пароль' 
    return render_template('lab4/login.html', error=error, authorized=False, login=login)

@lab4.route('/lab4/logout', methods = ['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')