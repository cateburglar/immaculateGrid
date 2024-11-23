import os

mysql = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "password"),
    "db": os.getenv("MYSQL_DATABASE", "seaquail"),
}
