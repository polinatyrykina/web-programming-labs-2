import os
from flask import Blueprint, render_template, request, jsonify, abort
import psycopg2
from psycopg2.extras import RealDictCursor

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/lab7.html')

films = [
    {
        "title": "Intouchables",
        "title_ru" : "1+1",
        "year": "2011",
        "description" : "Аристократ на коляске нанимает в сиделки бывшего заключенного.\
            Искрометная французская комедия с Омаром Си"
    },
    {
        "title": "Sen to Chihiro no kamikakushi",
        "title_ru" : "Унесённые призраками",
        "year": "2001",
        "description" : "Тихиро с мамой и папой переезжает в новый дом. \
            Заблудившись по дороге, они оказываются в странном пустынном городе, где\
            их ждет великолепный пир. Родители с жадностью набрасываются на еду \
            и к ужасу девочки превращаются в свиней, став пленниками злой колдуньи Юбабы. Теперь, оказавшись\
            одна среди волшебных существ и загадочных видений, Тихиро должна придумать, как избавить\
            своих родителей от чар коварной старухи."
    },
    {
        "title": "The Gentlemen",
        "title_ru" : "Джентльмены",
        "year": "2019",
        "description" : " Один ушлый американец ещё со студенческих лет приторговывал наркотиками,\
            а теперь придумал схему нелегального обогащения с использованием поместий обедневшей \
            английской аристократии и очень неплохо на этом разбогател. Другой пронырливый журналист\
            приходит к Рэю, правой руке американца, и предлагает тому купить киносценарий,\
            в котором подробно описаны преступления его босса при участии других представителей \
            лондонского криминального мира — партнёра-еврея, китайской диаспоры, чернокожих спортсменов \
            и даже русского олигарха."
    },
    {
        "title": "Green Book",
        "title_ru" : "Зеленая книга",
        "year": "2018",
        "description" : "1960-е годы. После закрытия нью-йоркского ночного клуба на \
            ремонт вышибала Тони по прозвищу Болтун ищет подработку на пару месяцев. \
            Как раз в это время Дон Ширли — утонченный светский лев, богатый и \
            талантливый чернокожий музыкант, исполняющий классическую музыку — собирается в турне \
            по южным штатам, где ещё сильны расистские убеждения и царит сегрегация. Он нанимает \
            Тони в качестве водителя, телохранителя и человека, способного решать текущие проблемы.\
            У этих двоих так мало общего, и эта поездка навсегда изменит жизнь обоих."
    },
    {
        "title": "The Help",
        "title_ru" : "Прислуга ",
        "year": "2011",
        "description" : "Американский Юг, на дворе 1960-е годы. Скитер только-только закончила\
            университет и возвращается домой, в сонный городок Джексон, где никогда ничего не\
            происходит. Она мечтает стать писательницей, вырваться в большой мир. Но для приличной\
            девушки с Юга не пристало тешиться столь глупыми иллюзиями, приличной девушке следует \
            выйти замуж и хлопотать по дому."
    },
]


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return films

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        abort(404, description="Film not found")
    return jsonify(films[id])


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id < 0 or id >= len(films):
        abort(404, description="Film not found")
    del films[id]
    return '',204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def update_film(id):
    if id < 0 or id >= len(films):
        abort(404, description="Film not found")

    updated_film = request.get_json()
    films[id] = updated_film
    return jsonify(films[id]), 200

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    new_film = request.get_json()
    films.append(new_film)
    new_index = len(films) - 1
    return jsonify({"id": new_index}), 201

