document.getElementById('loginForm').addEventListener('submit', async function (event) {
    event.preventDefault();

    try {
        await loginUser();
        alert('Login successful');

    } catch (error) {
        handleError(error);
    }
});

async function loginUser() {
    const formData = new FormData(document.getElementById('loginForm'));
    const response = await fetch('http://127.0.0.1:8000/users/token/login/', {
        method: 'POST',
        body: formData,
    });

    if (!response.ok) {
        throw new Error('Invalid username or password');
    }

    const data = await response.json();
    const token = data.auth_token;
    localStorage.setItem('authToken', token);
    window.location.href = "http://127.0.0.1:8000/all_users";
    return token;
}

function handleError(error) {
    console.error('Error:', error.message);
    alert('Login failed: ' + error.message);
}
