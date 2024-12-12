import os
from flask import Blueprint, render_template, request, jsonify, abort, session, current_app
import psycopg2
import sqlite3
from os import path
from psycopg2.extras import RealDictCursor

lab7 = Blueprint('lab7', __name__)

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host = '127.0.0.1',
            database = 'polina_tyrykina_knowledge_base',
            user = 'polina_tyrykina_knowledge_base',
            password = '123',
            client_encoding='UTF8'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur


def db_connect():
    conn = psycopg2.connect(
        host='127.0.0.1',
        database='polina_tyrykina_knowledge_base',
        user='polina_tyrykina_knowledge_base',
        password='123'
    )
    cur = conn.cursor(cursor_factory=RealDictCursor)
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()



@lab7.route('/lab7/')
def main():
    return render_template('lab7/lab7.html')

# films = [
#     {
#         "title": "Intouchables",
#         "title_ru" : "1+1",
#         "year": "2011",
#         "description" : "Аристократ на коляске нанимает в сиделки бывшего заключенного.\
#             Искрометная французская комедия с Омаром Си"
#     },
#     {
#         "title": "Sen to Chihiro no kamikakushi",
#         "title_ru" : "Унесённые призраками",
#         "year": "2001",
#         "description" : "Тихиро с мамой и папой переезжает в новый дом. \
#             Заблудившись по дороге, они оказываются в странном пустынном городе, где\
#             их ждет великолепный пир. Родители с жадностью набрасываются на еду \
#             и к ужасу девочки превращаются в свиней, став пленниками злой колдуньи Юбабы. Теперь, оказавшись\
#             одна среди волшебных существ и загадочных видений, Тихиро должна придумать, как избавить\
#             своих родителей от чар коварной старухи."
#     },
#     {
#         "title": "The Gentlemen",
#         "title_ru" : "Джентльмены",
#         "year": "2019",
#         "description" : " Один ушлый американец ещё со студенческих лет приторговывал наркотиками,\
#             а теперь придумал схему нелегального обогащения с использованием поместий обедневшей \
#             английской аристократии и очень неплохо на этом разбогател. Другой пронырливый журналист\
#             приходит к Рэю, правой руке американца, и предлагает тому купить киносценарий,\
#             в котором подробно описаны преступления его босса при участии других представителей \
#             лондонского криминального мира — партнёра-еврея, китайской диаспоры, чернокожих спортсменов \
#             и даже русского олигарха."
#     },
#     {
#         "title": "Green Book",
#         "title_ru" : "Зеленая книга",
#         "year": "2018",
#         "description" : "1960-е годы. После закрытия нью-йоркского ночного клуба на \
#             ремонт вышибала Тони по прозвищу Болтун ищет подработку на пару месяцев. \
#             Как раз в это время Дон Ширли — утонченный светский лев, богатый и \
#             талантливый чернокожий музыкант, исполняющий классическую музыку — собирается в турне \
#             по южным штатам, где ещё сильны расистские убеждения и царит сегрегация. Он нанимает \
#             Тони в качестве водителя, телохранителя и человека, способного решать текущие проблемы.\
#             У этих двоих так мало общего, и эта поездка навсегда изменит жизнь обоих."
#     },
#     {
#         "title": "The Help",
#         "title_ru" : "Прислуга ",
#         "year": "2011",
#         "description" : "Американский Юг, на дворе 1960-е годы. Скитер только-только закончила\
#             университет и возвращается домой, в сонный городок Джексон, где никогда ничего не\
#             происходит. Она мечтает стать писательницей, вырваться в большой мир. Но для приличной\
#             девушки с Юга не пристало тешиться столь глупыми иллюзиями, приличной девушке следует \
#             выйти замуж и хлопотать по дому."
#     },
# ]


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn, cur = db_connect()
    cur.execute("SELECT * FROM films;")
    films = cur.fetchall()
    db_close(conn, cur)
    return jsonify(films)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn, cur = db_connect()
    cur.execute("SELECT * FROM films WHERE id = %s;", (id,))
    film = cur.fetchone()
    db_close(conn, cur)
    if not film:
        abort(404, description="Фильм не найден")
    return jsonify(film)



@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def delete_film(id):
    conn, cur = db_connect()
    cur.execute("DELETE FROM films WHERE id = %s;", (id,))
    db_close(conn, cur)
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def update_film(id):
    """Обновить информацию о фильме"""
    film = request.get_json()
    title = film.get('title')
    title_ru = film.get('title_ru')
    year = film.get('year')
    description = film.get('description')

    try:
        year = int(year)
    except ValueError:
        return jsonify({'error': 'Год выпуска должен быть числом'}), 400

    if not title_ru or (not title and not title_ru):
        return jsonify({'error': 'Должно быть указано хотя бы одно название фильма (на русском или оригинальном)'}), 400
    if not description or len(description) > 2000:
        return jsonify({'error': 'Описание должно быть указано и не превышать 2000 символов'}), 400
    if not (1895 <= year <= 2024):
        return jsonify({'error': 'Год выпуска должен быть между 1895 и 2024'}), 400

    conn, cur = db_connect()
    cur.execute(
        "UPDATE films SET title = %s, title_ru = %s, year = %s, description = %s WHERE id = %s;",
        (title, title_ru, year, description, id)
    )
    db_close(conn, cur)

    return jsonify({'id': id}), 200

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    title = film.get('title')
    title_ru = film.get('title_ru')
    year = film.get('year')
    description = film.get('description')

    try:
        year = int(year)
    except ValueError:
        return jsonify({'year': 'Год выпуска должен быть числом'}), 400

    errors = {}
    if not title_ru and not title:
        errors['title'] = 'Должно быть указано хотя бы одно название фильма (на русском или оригинальном)'
    if not description or len(description) > 2000:
        errors['description'] = 'Описание должно быть указано и не превышать 2000 символов'
    if not (1895 <= year <= 2024):
        errors['year'] = 'Год выпуска должен быть между 1895 и 2024'

    if errors:
        return jsonify(errors), 400

    conn, cur = db_connect()
    cur.execute(
        "INSERT INTO films (title, title_ru, year, description) VALUES (%s, %s, %s, %s) RETURNING id;",
        (title, title_ru, year, description)
    )
    film_id = cur.fetchone()['id']
    db_close(conn, cur)

    return jsonify({'id': film_id}), 201
