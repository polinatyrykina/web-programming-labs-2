from flask import Blueprint, redirect, url_for
lab1 = Blueprint('lab1', __name__)

@lab1.route("/lab1")
def lab():
    return '''
<!DOCTYPE html>
<html>
<link rel = "stylesheet" href="''' + url_for('static', filename = 'lab1/main.css') + '''">
    <head>
        <title>Тырыкина Полина Анатольевна, лабораторная 1</title>
    </head>
    <body>
        <header>
            НГТУ, ФБ, Лабораторная работа 1
        </header>

        <h1>web-сервер на flask</h1>

        <p>Flask — фреймворк для создания веб-приложений на языке
        программирования Python, использующий набор инструментов
        Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
        называемых микрофреймворков — минималистичных каркасов веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
        </p>

        <a href="/menu">Меню</a>

        <h2>Реализованные роуты</h2>
        <ul>
            <li>
                <a href="/lab1/oak">Дуб</a>
            </li>
            <li>
                <a href="/lab1/student">Студент</a>
            </li>
            <li>
                <a href="/lab1/python">Python</a>
            </li>
            <li>
                <a href="/lab1/zemfira">Земфира</a>
            </li>
        </ul>

        <footer>
                &copy; Тырыкина Полина, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
'''

@lab1.route("/lab1/oak")
def oak():
    return '''
<!DOCTYPE html>
<html>
<link rel = "stylesheet" href="''' + url_for('static', filename = 'lab1/lab1.css') + '''">
    <body>
        <h1>Дуб</h1>

        <p>Дуб считается одним из самых красивых деревьев, к нему относятся с почтением и любовью. 
        Дуб обыкновенный, или черешчатый, растёт в европейской части России.Дуб - громадное дерево, до 40 м высотой, с толстым стволом и извилистыми крепкими сучьями, образующими широкий шатёр листвы. 
        Дубы очень любят свет, и их побеги меняют направление роста несколько раз в сезон - в зависимости от освещения. Ветви у старых дубов имеют причудливые изгибы. Дуб может прожить очень долго. 
        Срубят его, а от пня потянется к свету молодая поросль - толстые побеги с очень крупными листьями. Крупные они потому, что вся влага, которую выкачивают из земли мощные корни,
        поит теперь только их. Дуб боится морозов. Молодые листья и стебли весной погибают при заморозках. Чтобы уберечься от этой беды, дуб начинает зеленеть поздно, чуть ли не позднее всех деревьев. 
        От весны всего можно ждать, в том числе поздних заморозков.</p>
        
        <img src="''' + url_for('static', filename = 'lab1/oak.jpg') + ''' ">

    </body>
</html>
'''

@lab1.route("/lab1/student")
def student():
    return '''
<!DOCTYPE html>
<html>
<link rel = "stylesheet" href="''' + url_for('static', filename = 'lab1/lab1.css') + '''">
    <body>
        <h1>Тырыкина Полина Анатольевна</h1>
        <img src="''' + url_for('static', filename = 'lab1/NETI.png') + ''' ">
    </body>
</html>
'''

@lab1.route("/lab1/python")
def python():
    return '''
<!DOCTYPE html>
<html>
<link rel = "stylesheet" href="''' + url_for('static', filename = 'lab1/lab1.css') + '''">
    <body>
        <h1>Python как язык программирования</h1>
        <p>Python — это высокоуровневый язык программирования, отличающийся 
        эффективностью, простотой и универсальностью использования. Он широко
        применяется в разработке веб-приложений и прикладного программного 
        обеспечения, а также в машинном обучении и обработке больших данных. 
        За счет простого и интуитивно понятного синтаксиса является одним из
        распространенных языков для обучения программированию. </p>

        <p>Язык программирования Python был создан в 1989–1991 годах голландским 
        программистом Гвидо ван Россумом. Изначально это был любительский проект: 
        разработчик начал работу над ним, просто чтобы занять себя на рождественских 
        каникулах. Хотя сама идея создания нового языка появилась у него двумя годами 
        ранее. Имя ему Гвидо взял из своей любимой развлекательной передачи «Летающий цирк Монти Пайтона». </p>
        
        <img src="''' + url_for('static', filename = 'lab1/python.png') + ''' ">
    </body>
</html>
'''

@lab1.route("/lab1/zemfira")
def zemfira():
    return '''
<!DOCTYPE html>
<html>
<link rel = "stylesheet" href="''' + url_for('static', filename = 'lab1/lab1.css') + '''">
    <body>
        <h1>Тексты и тематика песен Земфиры</h1>
        <p>Тексты песен Земфиры отличаются своеобразием и неповторимым стилем. 
        Сама певица не любит рассказывать в интервью о текстах и не считает 
        себя поэтом. Вячеслав Огрызко в «Литературной газете» отмечал, что в одном 
        из интервью она упоминала: «Я всегда говорю, я не считаю, что пишу стихи». 
        Однако её тексты часто печатают в сборниках рок-поэзии.</p>

        <p>Музыкальный стиль Земфиры относят к жанрам рока и поп-рока. В её музыке находят
        влияние как гитарного попа, так и гармоний джаза и босса-новы. Майкл Зильберман 
        писал, что влияния на музыку певицы можно отыскать в произведениях нероссийских 
        артистов. </p>
        
        <img src="''' + url_for('static', filename = 'lab1/zemfira.jpg') + ''' ">
    </body>
</html>
'''