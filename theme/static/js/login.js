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
    const response = await fetch('https://littlelemon-api-se1c.onrender.com/users/users/login/', {
        method: 'POST',
        body: formData,
    });

    if (!response.ok) {
        throw new Error('Invalid username or password');
    }

    const data = await response.json();
    const token = data.auth_token;
    localStorage.setItem('authToken', token);
    window.location.href = "https://littlelemon-api-se1c.onrender.com/all_users/";
    return token;
}

function handleError(error) {
    console.error('Error:', error.message);
    alert('Login failed: ' + error.message);
}
