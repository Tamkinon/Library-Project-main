async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (username === 'admin' && password === 'admin123'){
        // redirect to index.html
        window.location.href = 'index.html';
        getGames();
        getUsers();
        getLoans();
    }
    else {
            alert('Login failed - Invalid credentials');
            console.error('Login error: Invalid credentials');
    }
}