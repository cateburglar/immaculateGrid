from ..extensions import db


class AllStarFull(db.Model):
    __tablename__ = "AllStarFull"
    allstarfull_ID = db.Column(db.Integer, primary_key=True, nullable=False)
    playerID = db.Column(
        db.String(9), db.foreign_key("people.playerID"), nullable=False
    )
    ldID = db.Column(db.Char(2), db.foreign_key("leagues.lgID"), nullable=False)
    teamID = db.Column(db.Char(3), nullable=False)
    yearID = db.Column(db.SmallInt(6), nullable=False)
    gameID = db.Column(db.String(12))
    GP = db.Column(db.SmallInt(6))
    startingPos = db.Column(db.SmallInt(6))
