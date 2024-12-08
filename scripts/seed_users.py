import os
import sys

from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

print(f"Project root added to sys.path: {project_root}")

import app.csi3335f2024 as cfg
from app import db
from app.models import User
from app.utils import create_enginestr_from_values, create_session_from_str


def seed_users():
    session = create_session_from_str(create_enginestr_from_values(cfg.mysql))
    if not session:
        print("Failed to create a database session.")
        return

    # Clear users
    session.execute(text("DELETE FROM USER where username is not null"))

    users = [
        User(
            username="admin",
            nameFirst="Admin",
            nameLast="User",
            password=generate_password_hash("password123", method="scrypt"),
            privilege="ADMIN",
            banned=False,
        ),
        User(
            username="john_doe",
            nameFirst="John",
            nameLast="Doe",
            password=generate_password_hash("password123", method="scrypt"),
            privilege="USER",
            banned=False,
        ),
        User(
            username="jane_doe",
            nameFirst="Jane",
            nameLast="Doe",
            password=generate_password_hash("password123", method="scrypt"),
            privilege="USER",
            banned=False,
        ),
        User(
            username="user1",
            nameFirst="User",
            nameLast="One",
            password=generate_password_hash("password123", method="scrypt"),
            privilege="USER",
            banned=False,
        ),
        User(
            username="user2",
            nameFirst="User",
            nameLast="Two",
            password=generate_password_hash("password123", method="scrypt"),
            privilege="USER",
            banned=False,
        ),
        User(
            username="user3",
            nameFirst="User",
            nameLast="Three",
            password=generate_password_hash("password123", method="scrypt"),
            privilege="USER",
            banned=False,
        ),
        User(
            username="user4",
            nameFirst="User",
            nameLast="Four",
            password=generate_password_hash("password123", method="scrypt"),
            privilege="USER",
            banned=False,
        ),
        User(
            username="user5",
            nameFirst="User",
            nameLast="Five",
            password=generate_password_hash("password123", method="scrypt"),
            privilege="USER",
            banned=False,
        ),
        User(
            username="user6",
            nameFirst="User",
            nameLast="Six",
            password=generate_password_hash("password123", method="scrypt"),
            privilege="USER",
            banned=False,
        ),
        User(
            username="user7",
            nameFirst="User",
            nameLast="Seven",
            password=generate_password_hash("password123", method="scrypt"),
            privilege="USER",
            banned=False,
        ),
        User(
            username="user8",
            nameFirst="User",
            nameLast="Eight",
            password=generate_password_hash("password123", method="scrypt"),
            privilege="USER",
            banned=False,
        ),
        User(
            username="user9",
            nameFirst="User",
            nameLast="Nine",
            password=generate_password_hash("password123", method="scrypt"),
            privilege="USER",
            banned=False,
        ),
        User(
            username="user10",
            nameFirst="User",
            nameLast="Ten",
            password=generate_password_hash("password123", method="scrypt"),
            privilege="USER",
            banned=False,
        ),
        User(
            username="user11",
            nameFirst="User",
            nameLast="Eleven",
            password=generate_password_hash("password123", method="scrypt"),
            privilege="USER",
            banned=False,
        ),
        User(
            username="user12",
            nameFirst="User",
            nameLast="Twelve",
            password=generate_password_hash("password123", method="scrypt"),
            privilege="USER",
            banned=False,
        ),
        User(
            username="user13",
            nameFirst="User",
            nameLast="Thirteen",
            password=generate_password_hash("password123", method="scrypt"),
            privilege="USER",
            banned=False,
        ),
        User(
            username="user14",
            nameFirst="User",
            nameLast="Fourteen",
            password=generate_password_hash("password123", method="scrypt"),
            privilege="USER",
            banned=False,
        ),
        User(
            username="user15",
            nameFirst="User",
            nameLast="Fifteen",
            password=generate_password_hash("password123", method="scrypt"),
            privilege="USER",
            banned=False,
        ),
        User(
            username="user16",
            nameFirst="User",
            nameLast="Sixteen",
            password=generate_password_hash("password123", method="scrypt"),
            privilege="USER",
            banned=False,
        ),
        User(
            username="user17",
            nameFirst="User",
            nameLast="Seventeen",
            password=generate_password_hash("password123", method="scrypt"),
            privilege="USER",
            banned=False,
        ),
        User(
            username="user18",
            nameFirst="User",
            nameLast="Eighteen",
            password=generate_password_hash("password123", method="scrypt"),
            privilege="USER",
            banned=False,
        ),
        User(
            username="user19",
            nameFirst="User",
            nameLast="Nineteen",
            password=generate_password_hash("password123", method="scrypt"),
            privilege="USER",
            banned=False,
        ),
        User(
            username="user20",
            nameFirst="User",
            nameLast="Twenty",
            password=generate_password_hash("password123", method="scrypt"),
            privilege="USER",
            banned=False,
        ),
    ]

    for user in users:
        session.add(user)

    try:
        session.commit()
        print("Users seeded successfully.")
    except IntegrityError as e:
        session.rollback()
        print(f"Error seeding users: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    seed_users()
