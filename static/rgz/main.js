// Функция для получения всех пользователей
async function fetchUsers() {
    const response = await fetch('/rgz/api/users');
    const users = await response.json();
    const usersList = document.getElementById('users-list');

    users.forEach(user => {
        const userCard = document.createElement('div');
        userCard.className = 'user-card';
        userCard.innerHTML = `
            <h3>${user.name}</h3>
            <p><strong>Вид услуги:</strong> ${user.service_type}</p>
            <p><strong>Стаж:</strong> ${user.experience} лет</p>
            <p><strong>Цена:</strong> ${user.price} руб.</p>
            <p><strong>О себе:</strong> ${user.about}</p>
        `;
        usersList.appendChild(userCard);
    });
}

// Вызов функции при загрузке страницы
document.addEventListener('DOMContentLoaded', fetchUsers);