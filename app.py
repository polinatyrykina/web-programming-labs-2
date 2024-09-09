from flask import Flask
app = Flask(__name__)

@app.route("/")
def start():
    return """
<!DOCTYPE html>
<html>
    <head>
        <title>Тырыкина Полина Анатольевна, лабораторная 1</title>
    </head>
    <body>
        <header>
            НГТУ, ФБ, Лабораторная работа 1
        </header>

        <h1>web-сервер на flask</h1>

        <footer>
                &copy; Тырыкина Полина, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
"""