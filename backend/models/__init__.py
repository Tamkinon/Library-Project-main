from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .loan import Loan
from .game import Game
from .user import User
from .admin import Admin