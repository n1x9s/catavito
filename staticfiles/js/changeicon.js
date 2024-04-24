// Предположим, что у вас есть переменная isAuthenticated, которая хранит статус аутентификации пользователя

function changeIcon() {
    const loginIcon = document.getElementById('login-icon');
    const profileIcon = document.getElementById('profile-icon');

    // Если пользователь авторизован, скрываем иконку логина и показываем иконку профиля
    if (isAuthenticated) {
        loginIcon.style.display = 'none';
        profileIcon.style.display = 'block';
    } else {
        // В противном случае показываем иконку логина и скрываем иконку профиля
        loginIcon.style.display = 'block';
        profileIcon.style.display = 'none';
    }
}

// Вызываем функцию changeIcon при загрузке страницы
window.onload = changeIcon;




