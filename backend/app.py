from flask import Flask, request, jsonify, session
from flask_cors import CORS
from datetime import datetime, timedelta
from models import db, Loan, Game, User, Admin
from werkzeug.security import generate_password_hash, check_password_hash
import logging
from datetime import datetime



app = Flask(__name__)  # - create a flask instance
# - enable all routes, allow requests from anywhere (optional - not recommended for security)
CORS(app, resources={r"/*": {"origins": "*"}})


# Specifies the database connection URL. In this case, it's creating a SQLite database
# named 'library.db' in your project directory. The three slashes '///' indicate a
# relative path from the current directory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games_store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'TamirBenDavid1'  # Required for session management
db.init_app(app)  # initializes the databsewith the flask application


# this is a decorator from the flask module to define a route for for adding a game, supporting POST requests.(check the decorator summary i sent you and also the exercises)
@app.route('/games', methods=['POST'])
def add_game():
    data = request.json  # this is parsing the JSON data from the request body
    new_game = Game(
        title=data['title'],  # Set the title of the new game.
        genre=data['genre'],  # Set the author of the new game.
        price=data['price'],
        # Set the types(fantasy, thriller, etc...) of the new game.
        quantity=data['quantity']
        # add other if needed...
    )
    db.session.add(new_game)  # add the bew game to the database session
    db.session.commit()  # commit the session to save in the database
    return jsonify({'message': 'Game added to database.'}), 201


# a decorator to Define a new route that handles GET requests
@app.route('/games', methods=['GET'])
def get_games():
    try:
        games = Game.query.all()                    # Get all the games from the database

        # Create empty list to store formatted game data we get from the database
        games_list = []

        for game in games:                         # Loop through each game from database
            game_data = {                          # Create a dictionary for each game
                'id': game.id,
                'title': game.title,
                'genre': game.genre,
                'price': game.price,
                'quantity': game.quantity
            }
            # Add the iterated game dictionary to our list
            games_list.append(game_data)

        return jsonify({                           # Return JSON response
            'message': 'games retrieved successfully',
            'games': games_list
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve games',
            'message': str(e)
        }), 500


@app.route('/login', methods=['POST'])
def add_admin():
    data = request.json  # this is parsing the JSON data from the request body
    new_admin = Admin(
        username=data['username'],  # Set the username of the new admin.
        password=data['password'],  # Set the password of the new admin.
    )
    db.session.add(new_admin)  # add the new admin to the database session
    db.session.commit()  # commit the session to save in the database
    return jsonify({'message': 'Game added to database.'}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    admin = Admin.query.filter_by(username=data['username']).first()

    if admin and check_password_hash(admin.password, data['password']):
        session['admin_id'] = admin.id
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('admin_id', None)
    return jsonify({'message': 'Logout successful'}), 200

# User management routes


@app.route('/users', methods=['POST'])
def add_user():
    # if 'admin_id' not in session:
    #     return jsonify({'message': 'Unauthorized'}), 401

    data = request.json
    new_user = User(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added successfully', 'user_id': new_user.id}), 201


@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()                    # Get all the users from the database

        # Create empty list to store formatted user data we get from the database
        users_list = []

        for user in users:                         # Loop through each game from database
            user_data = {                          # Create a dictionary for each game
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'phone': user.phone
            }
            # Add the iterated user dictionary to our list
            users_list.append(user_data)

        return jsonify({                           # Return JSON response
            'message': 'users retrieved successfully',
            'users': users_list
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve users',
            'message': str(e)
        }), 500

# Loan management routes

logging.basicConfig(level=logging.DEBUG)


@app.route('/loans', methods=['POST'])
def create_loan():
    data = request.json
    user_id = data['user_id']
    game_id = data['game_id']

    try:
        game = Game.query.get(game_id)
        if game is None:
            return jsonify({'message': 'Game not found!'}), 404
        if game.quantity > 0:
            game.quantity -= 1
            new_loan = Loan(user_id=user_id, game_id=game_id)
            db.session.add(new_loan)
            db.session.commit()
            return jsonify({'message': 'Loan created successfully!'}), 201
        else:
            return jsonify({'message': 'Game out of stock!'}), 400
    except Exception as e:
        logging.error(f"Error creating loan: {e}")
        return jsonify({'message': 'Failed to create loan'}), 500


@app.route('/loans/<int:loan_id>/return', methods=['POST'])
def return_loan(loan_id):
    loan = Loan.query.get(loan_id)
    if loan and not loan.is_returned:
        loan.return_date = datetime.utcnow()
        loan.is_returned = True
        game = Game.query.get(loan.game_id)
        game.quantity += 1
        db.session.commit()
        return jsonify({'message': 'Game returned successfully!'}), 200
    else:
        return jsonify({'message': 'Loan not found or already returned!'}), 404


@app.route('/loans', methods=['GET'])
def get_loans():
    loans = Loan.query.filter_by(return_date=None).all()
    loans_list = [{
        'id': loan.id,
        'user_id': loan.user_id,
        'game_id': loan.game_id,
        'loan_date': loan.loan_date.isoformat()
    } for loan in loans]
    return jsonify({'loans': loans_list}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create all database tables defined in your  models(check the models folder)

    # with app.test_client() as test:
    #     response = test.post('/login', json={  # Make a POST request to /games endpoint with game  data
    #         'username': 'admin',
    #         'password': 'admin123',
    #     })
    #     print("Testing /login endpoint:")
    #     # print the response from the server
    #     print(f"Response: {response.data}")

        #  GET test here
        # get_response = test.get('/games')
        # print("\nTesting GET /games endpoint:")
        # print(f"Response: {get_response.data}")

    app.run(debug=True)  # start the flask application in debug mode

    # DONT FORGET TO ACTIVATE THE ENV FIRST:
    # /env/Scripts/activate - for windows
    # source ./env/bin/activate - - mac
