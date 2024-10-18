from flask import Blueprint, redirect, url_for, request, make_response, render_template
lab3 = Blueprint('lab3', __name__)

@lab3.route("/lab3/")
def lab():
    name = request.cookies.get('name') or 'аноним' 
    name_color = request.cookies.get('name_color') 
    age = request.cookies.get('age') or 'неизвестный'  
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)

@lab3.route("/lab3/cookie")
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age = 5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp

@lab3.route("/lab3/del_cookie")
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp

@lab3.route("/lab3/form1")
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'

    age = request.args.get('age') 
    if age is None or age == '':
        errors['age'] = 'Заполните поле!'

    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)

@lab3.route("/lab3/order")
def order():
    return render_template('lab3/order.html')

@lab3.route("/lab3/pay")
def pay():
    price = 0
    drink = request.args.get('drink')
    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10
    return render_template('lab3/pay.html', price=price)

@lab3.route('/lab3/success')
def success():
    price = request.args.get('price')
    return render_template('lab3/success.html', price=price)

@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    background_color = request.args.get('background_color')
    font_size = request.args.get('font_size')
    font_family = request.args.get('font_family')
    
    resp = make_response(render_template('lab3/settings.html', color=color, background_color=background_color, font_size=font_size, font_family=font_family))
    
    if color or background_color or font_size or font_family:
        # Устанавливаем куки с новыми значениями
        if color:
            resp.set_cookie('color', color)
        if background_color:
            resp.set_cookie('background_color', background_color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        if font_family:
            resp.set_cookie('font_family', font_family)
        
        return resp  # Перенаправляем на тот же маршрут для обновления отображаемых значений
    
    return resp
@lab3.route('/lab3/settings/clear_cookies')
def clear_cookies():
    resp = make_response(redirect(url_for('lab3.settings')))

    resp.set_cookie('color', '', expires=0)
    resp.set_cookie('background_color', '', expires=0)
    resp.set_cookie('font_size', '', expires=0)
    resp.set_cookie('font_family', '', expires=0)

    return resp

@lab3.route("/lab3/ticket_form", methods=['GET', 'POST']) 
def ticket_form(): 
    errors = {}
    if request.method == 'POST':
        passenger_name = request.form.get('passenger_name')
        shelf_type = request.form.get('shelf_type')
        with_linen = request.form.get('with_linen')
        with_baggage = request.form.get('with_baggage')
        age = request.form.get('age')
        departure_point = request.form.get('departure_point')
        destination_point = request.form.get('destination_point')
        travel_date = request.form.get('travel_date')
        with_insurance = request.form.get('with_insurance')

        # Проверка на пустые поля
        if not all([passenger_name, shelf_type, age, departure_point, destination_point, travel_date]):
            flash("Все поля, кроме 'Багаж' и 'Страховка', должны быть заполнены!", "error")
            return redirect(url_for('lab3.ticket_form'))

        # Проверка возраста
        if not age.isdigit() or not (1 <= int(age) <= 120):
            flash("Возраст должен быть от 1 до 120 лет!", "error")
            return redirect(url_for('lab3.ticket_form'))

        # Расчет стоимости
        price = 1000 if int(age) >= 18 else 700
        if shelf_type in ['нижняЫя', 'нижняя боковая']:
            price += 100
        if with_linen == 'on':
            price += 75
        if with_baggage == 'on':
            price += 250
        if with_insurance == 'on':
            price += 150

        # Параметры для передачи в шаблон
        age_int = int(age)  # Преобразование возраста в целое число
        return render_template('lab3/ticket.html', 
                               passenger_name=passenger_name, 
                               shelf_type=shelf_type,
                               with_linen=with_linen, 
                               with_baggage=with_baggage, 
                               age=age_int,  # Отправляем как целое
                               departure_point=departure_point, 
                               destination_point=destination_point,
                               travel_date=travel_date, 
                               with_insurance=with_insurance,
                               price=price)

    return render_template('lab3/ticket_form.html', errors=errors)


books = [
    {'name': 'Зверобой', 'author': 'Купер Джеймс Фенимор', 'genre': 'Детская художественная литература', 'count': 480, 'price': 500, 'publisher': 'Эксмо', 'year': 2005},
    {'name': 'Шанхайская головоломка', 'author': 'Чэнь Ши', 'genre': 'Детективный роман', 'count': 288, 'price': 700, 'publisher': 'АСТ', 'year': 2012},
    {'name': 'Сюжет', 'author': 'Корелиц Джин', 'genre': 'Детективный роман', 'count': 480, 'price': 850, 'publisher': 'Рипол Классик', 'year': 2020},
    {'name': 'Сказать жизни "ДА!": психолог в концлагере', 'author': 'Франкл Виктор', 'genre': 'Психология личности', 'count': 239, 'price': 1200, 'publisher': 'Актион', 'year': 2018},
    {'name': 'Дом, в котором...', 'author': 'Петросян Мариам', 'genre': 'Современная проза', 'count': 944, 'price': 400, 'publisher': 'Молодая гвардия', 'year': 2019},
    {'name': 'Мара и Морок. Трилогия', 'author': 'Арден Лия', 'genre': 'Фэнтези', 'count': 800, 'price': 900, 'publisher': 'Эксмо', 'year': 2021},
    {'name': 'Ночь морлоков', 'author': 'Джетер Кевин Уэйн', 'genre': 'Научная фантастика', 'count': 320, 'price': 780, 'publisher': 'Астрель', 'year': 2015},
    {'name': 'Семья для чемпиона', 'author': 'Коваль Алекс', 'genre': 'Любовные романы', 'count': 480, 'price': 600, 'publisher': 'Иностранка', 'year': 2017},
    {'name': 'Клинок, рассекающий демонов. Том 1', 'author': 'Готогэ Коёхару', 'genre': 'Манга', 'count': 192, 'price': 500, 'publisher': 'Тесса', 'year': 2021},
    {'name': '1984', 'author': 'Джордж Оруэлл', 'genre': 'Драматургия', 'count': 150, 'price': 1500, 'publisher': 'Азбука', 'year': 2009},
    {'name': 'Мастер и Маргарита', 'author': 'Булгаков Михаил', 'genre': 'Роман', 'count': 370, 'price': 1000, 'publisher': 'Эксмо', 'year': 2011},
    {'name': 'Война и мир', 'author': 'Толстой Лев', 'genre': 'Роман', 'count': 1200, 'price': 2000, 'publisher': 'Правда', 'year': 2010},
    {'name': 'Гарри Поттер и философский камень', 'author': 'Роулинг Джоан', 'genre': 'Фэнтези', 'count': 600, 'price': 750, 'publisher': 'Росмэн', 'year': 2000},
    {'name': 'Пиковая дама', 'author': 'Пушкин Александр', 'genre': 'Сказка', 'count': 200, 'price': 250, 'publisher': 'Художественная литература', 'year': 1985},
    {'name': 'Унесенные ветром', 'author': 'Митчелл Маргарет', 'genre': 'Роман', 'count': 300, 'price': 1500, 'publisher': 'Наука', 'year': 2016},
    {'name': 'Фауст', 'author': 'Гёте Иоганн', 'genre': 'Трагедия', 'count': 444, 'price': 600, 'publisher': 'Атлант', 'year': 2020},
    {'name': 'Старик и море', 'author': 'Хемингуэй Эрнест', 'genre': 'Роман', 'count': 225, 'price': 450, 'publisher': 'Мир', 'year': 2014},
    {'name': 'Лолита', 'author': 'Набоков Владимир', 'genre': 'Роман', 'count': 310, 'price': 1200, 'publisher': 'Астрель', 'year': 2019},
    {'name': 'Маленький принц', 'author': 'Антуан де Сент-Экзюпери', 'genre': 'Сказка', 'count': 240, 'price': 400, 'publisher': 'Астрель', 'year': 2012}
]

@lab3.route('/lab3/search', methods=['GET'])
def search():
    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)
    
    filtered_books = []
    
    if min_price is not None and max_price is not None:
        filtered_books = [book for book in books if min_price <= book['price'] <= max_price]
    
    return render_template('lab3/search.html', books=filtered_books, min_price=min_price, max_price=max_price)