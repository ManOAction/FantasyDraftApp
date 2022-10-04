from datetime import datetime
from app import db
from sqlalchemy.sql import text


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship("Post", backref="author", lazy="dynamic")

    def __repr__(self):
        return "<User {}>".format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return "<Post {}>".format(self.body)


class DraftStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    CurrentTeam = db.Column(db.Integer, default=1)
    CurrentDraftPick = db.Column(db.Integer, default=1)
    DraftDirection = db.Column(db.Integer, default=1)
    TotalQB = db.Column(db.Integer, default=1)
    TotalRB = db.Column(db.Integer, default=2)
    TotalWR = db.Column(db.Integer, default=2)
    TotalTE = db.Column(db.Integer, default=1)
    TotalFLEX = db.Column(db.Integer, default=1)
    TotalDST = db.Column(db.Integer, default=1)
    TotalTeams = db.Column(db.Integer, default=12)

    def RemainingStarters(self):
        QBDrafted = (
            db.session.query(Player.id)
            .filter(Player.ownership_group > 0, Player.position == "QB")
            .count()
        )
        RBDrafted = (
            db.session.query(Player.id)
            .filter(Player.ownership_group > 0, Player.position == "RB")
            .count()
        )
        WRDrafted = (
            db.session.query(Player.id)
            .filter(Player.ownership_group > 0, Player.position == "WR")
            .count()
        )
        TEDrafted = (
            db.session.query(Player.id)
            .filter(Player.ownership_group > 0, Player.position == "WR")
            .count()
        )

        RQB = (self.TotalQB * 18) - QBDrafted
        RRB = (self.TotalRB * 18) - RBDrafted
        RWR = (self.TotalWR * 18) - WRDrafted
        RTE = (self.TotalTE * 18) - TEDrafted

        return RQB, RRB, RWR, RTE

    def PosVorp(self, Position):
        AlreadyDrafted = (
            db.session.query(Player.id)
            .filter(Player.ownership_group > 0, Player.position == Position)
            .count()
        )

        if Position == "QB":
            RemainingSlots = (self.TotalQB * self.TotalTeams) - AlreadyDrafted
        elif Position == "RB":
            RemainingSlots = (self.TotalRB * self.TotalTeams) - AlreadyDrafted
        elif Position == "WR":
            RemainingSlots = (self.TotalWR * self.TotalTeams) - AlreadyDrafted
        elif Position == "TE":
            RemainingSlots = (self.TotalTE * self.TotalTeams) - AlreadyDrafted

        else:
            RemaingSlots = 0

        TopPick = (
            Player.query.filter(
                Player.ownership_group == 0, Player.position == Position
            )
            .order_by(text("draftrank asc"))
            .first()
        )

        RelatedPicks = 0
        DraftRound = (
            Player.query.filter(Player.ownership_group == 0)
            .order_by(text("draftrank asc"))
            .limit(36)
        )

        for player in DraftRound:
            if player.position == Position:
                RelatedPicks += 1

        try:
            NextRoundPick = (
                Player.query.filter(
                    Player.pointprojection < TopPick.pointprojection,
                    Player.ownership_group == 0,
                    Player.position == Position,
                )
                .order_by(text("draftrank asc"))
                .offset(RelatedPicks)
                .first()
            )
        except Exception as errmsg:
            NextRoundPick = TopPick

        BottomPick = (
            Player.query.filter(
                Player.ownership_group == 0, Player.position == Position
            )
            .order_by(text("draftrank asc"))
            .offset(RemainingSlots)
            .first()
        )

        return TopPick, NextRoundPick, BottomPick

    def __repr__(self):
        return "<Currently Drafting {}>".format(self.CurrentTeam)


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    playername = db.Column(db.String(120), index=True, unique=True)
    position = db.Column(db.String(5), index=True, unique=False)
    team = db.Column(db.String(5), index=True, unique=False)
    tier = db.Column(db.Integer, index=True, default=0)
    draftrank = db.Column(db.Integer, index=True, default=0)
    pointprojection = db.Column(db.Integer, index=True, default=0)
    vorpatdraft = db.Column(db.Integer, default=0)
    ownership_group = db.Column(db.Integer, index=True, default=0)
    draft_pick = db.Column(db.Integer, default=0)

    def Vorp(self):

        RelatedPicks = 0

        DraftRound = (
            Player.query.filter(Player.ownership_group == 0)
            .order_by(text("draftrank asc"))
            .limit(36)
        )

        for player in DraftRound:
            if player.position == self.position:
                RelatedPicks += 1

        try:
            NextPlayer = (
                Player.query.filter(
                    Player.pointprojection < self.pointprojection,
                    Player.ownership_group == 0,
                    Player.position == self.position,
                )
                .order_by(text("draftrank asc"))
                .offset(RelatedPicks)
                .first()
            )
        except Exception as errmsg:
            NextPlayer = None

        if NextPlayer:
            VorpValue = self.pointprojection - NextPlayer.pointprojection

        else:
            VorpValue = 0

        return VorpValue

    def __repr__(self):
        return "<Player {}>".format(self.playername)
