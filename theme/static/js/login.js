document.getElementById('loginForm').addEventListener('submit', async function (event) {
    event.preventDefault();

    try {
        const token = await loginUser();
        console.log("Token: " + token);
        alert('Login successful');
    } catch (error) {
        console.log("Error al iniciar sesionar: " + error.message);
    }
});

async function loginUser() {
    const formData = new FormData(document.getElementById('loginForm'));

    const response = await fetch('https://littlelemon-api-se1c.onrender.com/login/', {
        method: 'POST',
        body: formData,
    });

    if (!response.ok) {
        const errorMessage = await response.text();
        console.error('Error en la solicitud:', errorMessage);
        throw new Error('Error en la solicitud al servidor');
    }

    const data = await response.json();
    const token = data.token;
    localStorage.setItem('authToken', token);
    window.location.href = "https://littlelemon-api-se1c.onrender.com/all_users/";
    return token;
}

function handleError(error) {
    console.error('Error:', error.message);
    alert('Login failed: ' + error.message);
}

// Función para obtener el valor del token CSRF desde las cookies
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}
