from . import db
from datetime import datetime 

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    loan_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    return_date = db.Column(db.DateTime)
    is_returned = db.Column(db.Boolean, default=False)

    def __init__(self, user_id, game_id):
        self.user_id = user_id
        self.game_id = game_id
        self.loan_date = datetime.utcnow()
        self.is_returned = False