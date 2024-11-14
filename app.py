from flask import Flask, redirect, url_for, render_template, session
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()


app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)

@app.route("/")
@app.route("/index")
def start():
    return redirect("/menu", code=302)

@app.route("/menu")
def menu():
    return '''
<!DOCTYPE html>
<html>
<link rel = "stylesheet" href="''' + url_for('static', filename = 'lab1/lab1.css') + '''">
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
        </header>

        <h1>web-сервер на flask</h1>
        <ul>
            <li>
                <a href="/lab1">Первая лабораторная</a>
            </li>
            <li>
                <a href="/lab2">Вторая лабораторная</a>
            </li>
            <li>
                <a href="/lab3">Третья лабораторная</a>
            </li>
            <li>
                <a href="/lab4">Четвертая лабораторная</a>
            </li>
            <li>
                <a href="/lab5">Пятая лабораторная</a>
            </li>
        </ul>
        <footer>
                &copy; Тырыкина Полина, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
'''
