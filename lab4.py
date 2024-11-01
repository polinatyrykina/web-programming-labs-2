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
]

@lab4.route('/lab4/login', methods=['GET', 'POST']) 
def login(): 
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login = session['login']
            matching_users = [user for user in users if user['login'] == login]
            user_name = matching_users[0]['name'] if matching_users else ''
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
            return redirect('/lab4/users')

    error = 'Неверные логин и/или пароль' 
    return render_template('lab4/login.html', error=error, authorized=False, login=login)

@lab4.route('/lab4/logout', methods = ['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    message = ""
    temperature = None

    if request.method == 'POST':
        temp_input = request.form.get('temperature')
        
        if temp_input == '':
            message = "Ошибка: не задана температура"
        else:
            try:
                temperature = float(temp_input)
            except ValueError:
                message = "Ошибка: некорректный ввод температуры"
                temperature = None
                return render_template('lab4/fridge.html', message=message)

            if temperature < -12:
                message = "Не удалось установить температуру — слишком низкое значение"
            elif temperature > -1:
                message = "Не удалось установить температуру — слишком высокое значение"
            elif -12 <= temperature <= -9:
                message = f"Установлена температура: {temperature}°C &#10052;&#10052;&#10052;"
            elif -8 <= temperature <= -5:
                message = f"Установлена температура: {temperature}°C &#10052;&#10052;"
            elif -4 <= temperature <= -1:
                message = f"Установлена температура: {temperature}°C &#10052;"

    return render_template('lab4/fridge.html', message=message, temperature=temperature)

grain_prices = {
    'ячмень': 12345,
    'овёс': 8522,
    'пшеница': 8722,
    'рожь': 14111
}

@lab4.route('/lab4/order-grain', methods=['GET', 'POST'])
def order_grain():
    message = ""
    if request.method == 'POST':
        grain_type = request.form.get('grain')
        weight_input = request.form.get('weight')
        
        if not weight_input:
            message = "Ошибка: не задан вес."
        else:
            try:
                weight = float(weight_input)
            except ValueError:
                message = "Ошибка: некорректный ввод веса."
                weight = 0

            if weight <= 0:
                message = "Ошибка: вес должен быть больше 0."
            elif weight > 500:
                message = "Ошибка: такого объёма сейчас нет в наличии."
            else:
                price_per_ton = grain_prices.get(grain_type, 0)
                total_price = weight * price_per_ton

                discount = 0
                if weight > 50:
                    discount = total_price * 0.10
                    total_price -= discount
                    discount_message = f"Применена скидка за большой объём: {discount:.2f} руб."
                else:
                    discount_message = ""

                message = (f"Заказ успешно сформирован. Вы заказали {grain_type}. "
                           f"Вес: {weight} т. Сумма к оплате: {total_price:.2f} руб. "
                           f"{discount_message}")

    return render_template('lab4/order_grain.html', message=message)

@lab4.route('/lab4/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')

        # Проверка на заполненность полей
        if not name or not login or not password:
            error = 'Все поля обязательны для заполнения.'
            return render_template('lab4/register.html', error=error)
        
        if any(user['login'] == login for user in users):
            error = 'Этот логин уже занят.'
            return render_template('lab4/register.html', error=error)
        
        # Регистрация нового пользователя
        users.append({'name': name, 'login': login, 'password': password})
        return redirect('/lab4/login')  # Перенаправление на страницу логина

    return render_template('lab4/register.html')

@lab4.route('/lab4/users', methods=['GET'])
def users1():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    return render_template('lab4/users.html', users=users)

@lab4.route('/lab4/delete/<user_login>', methods=['POST'])
def delete_user(user_login):
    global users
    users = [user for user in users if user['login'] != user_login]
    return redirect('/lab4/users')

@lab4.route('/lab4/edit/<user_login>', methods=['GET', 'POST'])
def edit_user(user_login):
    user = next((u for u in users if u['login'] == user_login), None)

    if request.method == 'POST':
        new_name = request.form.get('name')
        new_password = request.form.get('password')

        # Проверка на заполненность полей
        if not new_name or not new_password:
            error = 'Все поля обязательны для заполнения.'
            return render_template('lab4/edit.html', user=user, error=error)
        
        # Изменение данных пользователя
        user['name'] = new_name
        user['password'] = new_password
        
        return redirect('/lab4/users')

    return render_template('lab4/edit.html', user=user)