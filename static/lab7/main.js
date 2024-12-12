function fillFilmList() {
    fetch('/lab7/rest-api/films/')
    .then(function (data) {
        return data.json();
    })
    .then(function (films) {
        let tbody = document.getElementById('film-list');
        tbody.innerHTML = '';
        for (let i = 0; i < films.length; i++) {
            let tr = document.createElement('tr');

            let tdTitle = document.createElement('td');
            let tdTitleRus = document.createElement('td');
            let tdYear = document.createElement('td');
            let tdActions = document.createElement('td');

            tdTitleRus.innerText = films[i].title == films[i].title_ru ? '' : films[i].title;
            tdTitle.innerText = films[i].title_ru;
            tdYear.innerText = films[i].year;

            let editButton = document.createElement('button');
            editButton.innerText = 'Редактировать';
            editButton.onclick = function () {
                editFilm(i);
            };

            let delButton = document.createElement('button');
            delButton.innerText = 'Удалить';
            delButton.onclick = function () {
                deleteFilm(i, films[i].title_ru);
            };

            tdActions.append(editButton);
            tdActions.append(delButton);

            tr.append(tdTitle);
            tr.append(tdTitleRus);
            tr.append(tdYear);
            tr.append(tdActions);

            tbody.append(tr);
        }
    });
}

function deleteFilm(id, title) {
    if (!confirm(`Вы точно хотите удалить фильм "${title}"?`)) 
        return;

    fetch(`/lab7/rest-api/films/${id}`, { method: 'DELETE' })
        .then(function () {
            fillFilmList();
        })
}

function showModal() {
    document.querySelector('div.modal').style.display = 'block';
}

function hideModal() {
    document.querySelector('div.modal').style.display = 'none';
}

function cancel() {
    hideModal();
}

function addFilm() {
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    showModal();
}

function sendFilm() {
    const id = document.getElementById('id').value; // Получаем id из поля ввода
    const film = {
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title-ru').value,
        year: document.getElementById('year').value,
        description: document.getElementById('description').value
    };

    const url = `/lab7/rest-api/films/${id}`; // Используем id для обновления
    const method = id ? 'PUT' : 'POST'; // Если id есть, используем PUT, иначе POST

    fetch(url, {
        method: method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(film)
    })
    .then(function (response) {
        if (!response.ok) {
            throw new Error('Ошибка при обновлении/добавлении фильма');
        }
        return response.json();
    })
    .then(function () {
        fillFilmList(); // Обновляем список фильмов
        hideModal(); // Скрываем модальное окно
    })
    .catch(function (error) {
        console.error('Ошибка:', error);
    });
}

function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
    .then(function (data) {
        return data.json();
    })
    .then(function (film) {
        document.getElementById('id').value = id; // Устанавливаем id в поле ввода
        document.getElementById('title').value = film.title;
        document.getElementById('title-ru').value = film.title_ru;
        document.getElementById('year').value = film.year;
        document.getElementById('description').value = film.description;
        showModal();
    })
    .catch(function (error) {
        console.error('Ошибка при загрузке данных фильма:', error);
    });
}

fillFilmList();