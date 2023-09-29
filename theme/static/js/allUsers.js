console.log("Hola");

document.addEventListener('DOMContentLoaded', function () {
    // Asignar la función al evento onclick del botón
    const button = document.getElementById('btnFetch');
    button.addEventListener('click', loadAndRenderUserList);
});

async function loadAndRenderUserList() {
    const token = localStorage.getItem('authToken');

    try {
        const users = await fetchUserList(token);
        renderUserGrid(users);
    } catch (error) {
        handleError(error);
    }
}

async function fetchUserList(token) {
    const response = await fetch('https://littlelemon-api-se1c.onrender.com/users/users/', {
        method: 'GET',
        headers: {
            'Authorization': `Token ${token}`,
        },
    });

    if (!response.ok) {
        throw new Error('Failed to fetch user data');
    }

    return response.json();
}

function renderUserGrid(users) {
    const userDiv = document.getElementById('userDiv');

    // Crear la tabla
    const table = document.createElement('table');
    table.classList.add('min-w-full', 'bg-white', 'border', 'border-gray-300', 'shadow-lg', 'rounded-md', 'overflow-hidden');

    // Crear la fila de encabezado
    const headerRow = document.createElement('tr');
    headerRow.classList.add('bg-gray-50');
    const usernameHeader = document.createElement('th');
    usernameHeader.classList.add('px-6', 'py-3', 'text-left', 'font-medium', 'text-red-500', 'uppercase', 'tracking-wider');
    usernameHeader.textContent = 'Username';
    const emailHeader = document.createElement('th');
    emailHeader.classList.add('px-6', 'py-3', 'text-left', 'font-medium', 'text-gray-500', 'uppercase', 'tracking-wider');
    emailHeader.textContent = 'Email';
    headerRow.appendChild(usernameHeader);
    headerRow.appendChild(emailHeader);
    table.appendChild(headerRow);

    // Agregar filas para cada usuario
    users.forEach(user => {
        const userRow = document.createElement('tr');
        const usernameCell = document.createElement('td');
        usernameCell.classList.add('px-6', 'py-4', 'whitespace-nowrap', 'text-sm', 'text-gray-900');
        usernameCell.textContent = user.username;
        const emailCell = document.createElement('td');
        emailCell.classList.add('px-6', 'py-4', 'whitespace-nowrap', 'text-sm', 'text-gray-900');
        emailCell.textContent = user.email;
        userRow.appendChild(usernameCell);
        userRow.appendChild(emailCell);
        table.appendChild(userRow);
    });

    // Limpiar el contenedor y agregar la tabla
    userDiv.innerHTML = '';
    userDiv.appendChild(table);
}


function handleError(error) {
    console.error('Error:', error.message);
    alert('Failed to fetch user data: ' + error.message);
}