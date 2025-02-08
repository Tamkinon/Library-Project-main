// App initialization function
async function initializeApp() {
    try {
        await getGames();
        await getUsers();
        await populateLoanForm();
        await getLoans();
    } catch (error) {
        console.error('Error initializing app:', error);
    }
}


// Authentication functions
async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (username === 'admin' && password === 'admin123') {
        document.getElementById('auth-section').classList.add('hidden');
        document.getElementById('main-section').classList.remove('hidden');
        document.getElementById('games-section').classList.remove('hidden');
        document.getElementById('users-section').classList.remove('hidden');
        document.getElementById('loans-section').classList.remove('hidden');
        document.getElementById('add-game-form').classList.remove('hidden');
        document.getElementById('add-user-form').classList.remove('hidden');
        document.getElementById('create-loan-form').classList.remove('hidden');
        getGames();
        getUsers();
        getLoans();
    } else {
        alert('Login failed');
        console.error('Login error: Invalid credentials');
    }
}

async function logout() {
    try {
        await axios.post('http://127.0.0.1:5000/logout');
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
        const response = await axios.get('http://127.0.0.1:5000/loans');
        const loansList = document.getElementById('loaned-games-list');
        loansList.innerHTML = '';

        response.data.loans.forEach(loan => {
            if (!loan.is_returned) {
                loansList.innerHTML += `
                    <div class="loan-card">
                        <p>User ID: ${loan.user_id}</p>
                        <p>Game ID: ${loan.game_id}</p>
                        <p>Loan Date: ${new Date(loan.loan_date).toLocaleDateString()}</p>
                        <button id="return-button-${loan.id}" class="return-button" onclick="returnLoan(${loan.id})">Return Game</button>
                    </div>
                `;
            }
        });
    } catch (error) {
        console.error('Error fetching loans:', error);
    }
}

async function createLoan(userId = null, gameId = null) {
    if (!userId) {
        userId = document.getElementById('loan-user').value;
        if (!userId) return;
    }
    
    if (!gameId) {
        gameId = document.getElementById('loan-game').value;
        if (!gameId) return;
    }

    try {
        const response = await axios.post('http://127.0.0.1:5000/loans', {
            user_id: parseInt(userId),
            game_id: parseInt(gameId)
        });

        if (response.status === 201) {
            getLoans();
            getGames();
            alert('Loan created successfully!');
        } else {
            alert(response.data.message);
        }
    } catch (error) {
        console.error('Error creating loan:', error);
        alert('Failed to create loan');
    }
}

async function returnLoan(loanId) {
    try {
        await axios.post(`http://127.0.0.1:5000/loans/${loanId}/return`);
        getLoans();
        getGames();
        alert('Game returned successfully!');
    } catch (error) {
        console.error('Error returning loan:', error);
        alert('Failed to return game');
    }
}

// Populate loan form dropdowns
async function populateLoanForm() {
    try {
        const usersResponse = await axios.get('http://127.0.0.1:5000/users');
        const gamesResponse = await axios.get('http://127.0.0.1:5000/games');
        
        const loanUserSelect = document.getElementById('loan-user');
        const loanGameSelect = document.getElementById('loan-game');
        
        loanUserSelect.innerHTML = '<option value="">Select User</option>';
        loanGameSelect.innerHTML = '<option value="">Select Game</option>';
        
        usersResponse.data.users.forEach(user => {
            loanUserSelect.innerHTML += `<option value="${user.id}">${user.name}</option>`;
        });
        
        gamesResponse.data.games.forEach(game => {
            loanGameSelect.innerHTML += `<option value="${game.id}">${game.title}</option>`;
        });
    } catch (error) {
        console.error('Error populating loan form:', error);
    }
}

function scrollToSection(sectionId) {
    document.getElementById(sectionId).scrollIntoView({ behavior: 'smooth' });
}

// Load all data when page loads
document.addEventListener('DOMContentLoaded', initializeApp);