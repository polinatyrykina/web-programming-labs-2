from flask import Blueprint, render_template, request, redirect, url_for

lab9 = Blueprint('lab9', __name__)

user_data = {}

@lab9.route('/lab9/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        user_data['name'] = request.form['name']
        return redirect(url_for('lab9.age'))
    return render_template('lab9/index.html')

@lab9.route('/age', methods=['GET', 'POST'])
def age():
    if request.method == 'POST':
        user_data['age'] = request.form['age']
        return redirect(url_for('lab9.gender'))
    return render_template('lab9/age.html')

@lab9.route('/gender', methods=['GET', 'POST'])
def gender():
    if request.method == 'POST':
        user_data['gender'] = request.form['gender']
        return redirect(url_for('lab9.preference'))
    return render_template('lab9/gender.html')

@lab9.route('/preference', methods=['GET', 'POST'])
def preference():
    if request.method == 'POST':
        user_data['preference'] = request.form['preference']
        return redirect(url_for('lab9.sub_preference'))
    return render_template('lab9/preference.html')

@lab9.route('/sub_preference', methods=['GET', 'POST'])
def sub_preference():
    if request.method == 'POST':
        user_data['sub_preference'] = request.form['sub_preference']
        return redirect(url_for('lab9.congratulations'))
    return render_template('lab9/sub_preference.html', preference=user_data['preference'])

@lab9.route('/congratulations')
def congratulations():
    if not user_data.get('name') or not user_data.get('age') or not user_data.get('gender') or not user_data.get('preference') or not user_data.get('sub_preference'):
        return redirect(url_for('lab9.main'))

    name = user_data['name']
    age = int(user_data['age'])
    gender = user_data['gender']
    preference = user_data['preference']
    sub_preference = user_data['sub_preference']

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

    return render_template('lab9/congratulations.html', greeting=greeting, gift=gift, image=image)

