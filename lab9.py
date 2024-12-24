from flask import Blueprint, render_template, request, redirect, url_for, session

lab9 = Blueprint('lab9', __name__)

@lab9.route('/lab9/', methods=['GET', 'POST'])
def main():
    # Проверяем, есть ли сохраненные данные в сессии
    if 'greeting' in session and 'gift' in session and 'image' in session:
        greeting = session['greeting']
        gift = session['gift']
        image = session['image']
        return render_template('lab9/congratulations.html', greeting=greeting, gift=gift, image=image)

    # Если данных нет, отображаем форму для ввода имени
    if request.method == 'POST':
        session['name'] = request.form['name']
        return redirect(url_for('lab9.age'))
    return render_template('lab9/index.html')

@lab9.route('/age', methods=['GET', 'POST'])
def age():
    if request.method == 'POST':
        session['age'] = request.form['age']
        return redirect(url_for('lab9.gender'))
    return render_template('lab9/age.html')

@lab9.route('/gender', methods=['GET', 'POST'])
def gender():
    if request.method == 'POST':
        session['gender'] = request.form['gender']
        return redirect(url_for('lab9.preference'))
    return render_template('lab9/gender.html')

@lab9.route('/preference', methods=['GET', 'POST'])
def preference():
    if request.method == 'POST':
        session['preference'] = request.form['preference']
        return redirect(url_for('lab9.sub_preference'))
    return render_template('lab9/preference.html')

@lab9.route('/sub_preference', methods=['GET', 'POST'])
def sub_preference():
    if request.method == 'POST':
        session['sub_preference'] = request.form['sub_preference']
        return redirect(url_for('lab9.congratulations'))
    return render_template('lab9/sub_preference.html', preference=session['preference'])

@lab9.route('/congratulations')
def congratulations():
    # Проверяем, есть ли все необходимые данные в сессии
    if not session.get('name') or not session.get('age') or not session.get('gender') or not session.get('preference') or not session.get('sub_preference'):
        return redirect(url_for('lab9.main'))

    name = session['name']
    age = int(session['age'])
    gender = session['gender']
    preference = session['preference']
    sub_preference = session['sub_preference']

    # Генерация поздравления
    if gender == 'male':
        greeting = 'Поздравляю тебя, ' + name + ', желаю, чтобы все мечты исполнялись, чтобы ты всегда занимался тем, что нравится и приносит счастье!'
    else:
        greeting = 'Поздравляю тебя, ' + name + ', желаю, чтобы все мечты исполнялись, чтобы ты всегда занималась тем, что нравится и приносит счастье!'

    if preference == 'вкусное':
        if sub_preference == 'сладкое':
            gift = 'конфетки'
            image = 'candies.jpg'
        else:
            gift = 'большой кусок пиццы'
            image = 'pizza.jpg'
    else:
        if sub_preference == 'красивое':
            gift = 'букет цветов'
            image = 'flowers.jpg'
        else:
            gift = 'картина'
            image = 'painting.jpg'

    # Сохраняем данные в сессии
    session['greeting'] = greeting
    session['gift'] = gift
    session['image'] = image

    return render_template('lab9/congratulations.html', greeting=greeting, gift=gift, image=image)

@lab9.route('/reset')
def reset():
    # Очищаем сессию для сброса данных
    session.clear()
    return redirect(url_for('lab9.main'))
