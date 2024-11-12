from flask_login import UserMixin

from app import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    privilege = db.Column(db.String(5), nullable=False)

    @property
    def role(self):
        return "ADMIN" if self.privilege == "ADMIN" else "USER"


from app import login_manager


# Load user by ID for session management
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
