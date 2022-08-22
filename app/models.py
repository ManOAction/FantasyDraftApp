from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class DraftStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    CurrentTeam = db.Column(db.Integer, default=1)
    CurrentDraftPick = db.Column(db.Integer, default=1)
    DraftDirection = db.Column(db.Integer, default=1)
    TotalQB = db.Column(db.Integer, default=1)
    TotalRB = db.Column(db.Integer, default=2)
    TotalWR = db.Column(db.Integer, default=2)
    TotalTE = db.Column(db.Integer, default=1)
    TotalFLEX = db.Column(db.Integer, default=2)
    TotalDST = db.Column(db.Integer, default=1)
    TotalTeams = db.Column(db.Integer, default=12)
    
    def __repr__(self):
        return '<Currently Drafting {}>'.format(self.CurrentTeam)        

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    playername = db.Column(db.String(120), index=True, unique=True)
    position = db.Column(db.String(5), index=True, unique=False)
    tier = db.Column(db.String(5), index=True, unique=False)
    pointprojection = db.Column(db.Integer, default=0)
    vorpatdraft = db.Column(db.Integer, default=0)
    ownership_group = db.Column(db.Integer, default=0)

    def Vorp(self):
        
        return self.id
        # return Player.query.filter(Player.id == PlayerID).first()
        # Player.CalcVorp(id)

    def __repr__(self):
        return '<Player {}>'.format(self.playername)