from flask import Blueprint, redirect, url_for, render_template
lab2 = Blueprint('lab2', __name__)

@lab2.route("/lab2/example")
def example():
    name = 'Тырыкина Полина'
    lab_num = '2'
    group = '23'
    course = '3'
    fruits = [
        {'name':'яблоки', 'price':100},
        {'name':'груши', 'price':120},
        {'name':'апельсины', 'price':80},
        {'name':'мандарины', 'price':85},
        {'name':'манго', 'price':321}
    ]
    books = [
        {'name':'Зверобой', 'author': 'Купер Джеймс Фенимор', 'genre':'Детская художественная литература', 'count':480},
        {'name':'Шанхайская головоломка', 'author': 'Чэнь Ши', 'genre':'Детективный роман', 'count':288},
        {'name':'Сюжет', 'author': 'Корелиц Джин', 'genre':'Детективный роман', 'count':480},
        {'name':'Сказать жизни "ДА!": психолог в концлагере', 'author': 'Франкл Виктор', 'genre':'Психология личности.', 'count':239},
        {'name':'Дом, в котором...', 'author': 'Петросян Мариам', 'genre':'Современная проза', 'count':944},
        {'name':'Мара и Морок. Трилогия', 'author': 'Арден Лия', 'genre':'Фэнтези', 'count':800},
        {'name':'Ночь морлоков', 'author': 'Джетер Кевин Уэйн', 'genre':'Научная фантастика', 'count':320},
        {'name':'Семья для чемпиона', 'author': 'Коваль Алекс', 'genre':'Любовные романы', 'count':480},
        {'name':'Клинок, рассекающий демонов. Том 1 ', 'author': 'Готогэ Коёхару', 'genre':'Манга', 'count':192},
    ]
    return render_template('example.html', name=name, lab_num=lab_num, 
                           group=group, course=course, fruits=fruits, books=books)

@lab2.route("/lab2/")
def lab():
    return render_template('lab2.html')

@lab2.route("/lab2/cat")
def cat():
    return render_template('cat.html')