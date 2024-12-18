document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

    const response = await fetch('/rgz/api/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });

    const result = await response.json();

    if (response.ok) {
        alert(result.message);
        window.location.href = '/rgz/login';
    } else {
        alert(result.error);
    }
});