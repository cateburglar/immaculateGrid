import os


class Config:
    mysql = {
        "location": os.getenv("MYSQL_LOCATION", "localhost"),
        "user": os.getenv("MYSQL_USER", "web"),
        "password": os.getenv("MYSQL_PASSWORD", "mypass"),
        "database": os.getenv("MYSQL_DATABASE", "sea_quail"),
    }

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{mysql['user']}:{mysql['password']}@{mysql['location']}/{mysql['database']}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
