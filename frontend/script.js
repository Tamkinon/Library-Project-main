// Authentication functions
async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await axios.post('http://127.0.0.1:5000/login', {
            username,
            password
        }, { withCredentials: true });
        
        if (response.status === 200) {
            document.getElementById('auth-section').classList.add('hidden');
            document.getElementById('main-section').classList.remove('hidden');
            getGames();
            getUsers();
            getLoans();
        }
    } catch (error) {
        alert('Login failed');
        console.error('Login error:', error);
    }
}

async function logout() {
    try {
        await axios.post('http://127.0.0.1:5000/logout', {}, { withCredentials: true });
        document.getElementById('auth-section').classList.remove('hidden');
        document.getElementById('main-section').classList.add('hidden');
    } catch (error) {
        console.error('Logout error:', error);
    }
}

// function to get all games from the API
async function getGames() {
    try {
        const response = await axios.get('http://127.0.0.1:5000/games');
        const gamesList = document.getElementById('games-list');
        gamesList.innerHTML = ''; // Clear existing list

        response.data.games.forEach(game => {
            gamesList.innerHTML += `
                <div class="game-card">
                    <h3>${game.title}</h3>
                    <p>Genre: ${game.genre}</p>
                    <p>Price: ${game.price}</p>
                    <p>Quantity: ${game.quantity}</p>
                </div>
            `;
        });
    } catch (error) {
        console.error('Error fetching games:', error);
        alert('Failed to load games');
    }
}

async function addGame() {
    const title = document.getElementById('game-title').value;
    const genre = document.getElementById('game-genre').value;
    const price = document.getElementById('game-price').value;
    const quantity = document.getElementById('game-quantity').value;

    try {
        await axios.post('http://127.0.0.1:5000/games', {
            title: title,
            genre: genre,
            price: parseInt(price),
            quantity: parseInt(quantity)
        });
        
        // Clear form fields
        document.getElementById('game-title').value = '';
        document.getElementById('game-genre').value = '';
        document.getElementById('game-price').value = '';
        document.getElementById('game-quantity').value = '';

        // Refresh the games list
        getGames();
        
        alert('Game added successfully!');
    } catch (error) {
        console.error('Error adding game:', error);
        alert('Failed to add game');
    }
}

// User management functions
async function getUsers() {
    try {
        const response = await axios.get('http://127.0.0.1:5000/users');
        const usersList = document.getElementById('users-list');
        usersList.innerHTML = ''; // Clear existing list

        response.data.users.forEach(user => {
            usersList.innerHTML += `
                <div class="user-card">
                    <h3>${user.name}</h3>
                    <p>Email: ${user.email}</p>
                    <p>Phone: ${user.phone}</p>
                </div>
            `;
        });
    } catch (error) {
        console.error('Error fetching users:', error);
        alert('Failed to load users');
    }
}

async function addUser() {
    const name = document.getElementById('user-name').value;
    const email = document.getElementById('user-email').value;
    const phone = document.getElementById('user-phone').value;

    try {
        await axios.post('http://127.0.0.1:5000/users', {
            name: name,
            email: email,
            phone: phone,
        });
        
        // Clear form fields
        document.getElementById('user-name').value = '';
        document.getElementById('user-email').value = '';
        document.getElementById('user-phone').value = '';

        // Refresh the games list
        getUsers();
        
        alert('User added successfully!');
    } catch (error) {
        console.error('Error adding user:', error);
        alert('Failed to add user');
    }
}

// Loan management functions
async function getLoans() {
    try {
        const response = await axios.get('http://127.0.0.1:5000/loans', { withCredentials: true });
        const loansList = document.getElementById('loaned-games-list');
        loansList.innerHTML = '';

        response.data.loans.forEach(loan => {
            loansList.innerHTML += `
                <div class="loan-card">
                    <p>User ID: ${loan.user_id}</p>
                    <p>Game ID: ${loan.game_id}</p>
                    <p>Loan Date: ${new Date(loan.loan_date).toLocaleDateString()}</p>
                    <button onclick="returnLoan(${loan.id})">Return Game</button>
                </div>
            `;
        });
    } catch (error) {
        console.error('Error fetching loans:', error);
    }
}

async function createLoan(userId = null, gameId = null) {
    if (!userId) {
        userId = prompt('Enter User ID:');
        if (!userId) return;
    }
    
    if (!gameId) {
        gameId = prompt('Enter Game ID:');
        if (!gameId) return;
    }

    try {
        await axios.post('http://127.0.0.1:5000/loans', {
            user_id: parseInt(userId),
            game_id: parseInt(gameId)
        }, { withCredentials: true });

        getLoans();
        getGames();
        alert('Loan created successfully!');
    } catch (error) {
        console.error('Error creating loan:', error);
        alert('Failed to create loan');
    }
}

async function returnLoan(loanId) {
    try {
        await axios.post(`http://127.0.0.1:5000/loans/${loanId}/return`, {}, { withCredentials: true });
        getLoans();
        getGames();
        alert('Game returned successfully!');
    } catch (error) {
        console.error('Error returning loan:', error);
        alert('Failed to return game');
    }
}

// Load all data when page loads
document.addEventListener('DOMContentLoaded', getGames);
document.addEventListener('DOMContentLoaded', getUsers);