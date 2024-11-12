import os
import sys

from sqlalchemy.exc import IntegrityError

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import app.csi3335f2024 as cfg
from app import db
from app.models import User
from app.utils import create_enginestr_from_values, create_session_from_str


def seed_users():
    session = create_session_from_str(create_enginestr_from_values(cfg.mysql))
    if not session:
        print("Failed to create a database session.")
        return

    users = [
        User(
            username="admin",
            nameFirst="Admin",
            nameLast="User",
            password="adminpassword",
            privilege="ADMIN",
            banned=False,
        ),
        User(
            username="john_doe",
            nameFirst="John",
            nameLast="Doe",
            password="password123",
            privilege="USER",
            banned=False,
        ),
        User(
            username="jane_doe",
            nameFirst="Jane",
            nameLast="Doe",
            password="password123",
            privilege="USER",
            banned=False,
        ),
        User(
            username="user1",
            nameFirst="User",
            nameLast="One",
            password="password123",
            privilege="USER",
            banned=False,
        ),
        User(
            username="user2",
            nameFirst="User",
            nameLast="Two",
            password="password123",
            privilege="USER",
            banned=False,
        ),
        User(
            username="user3",
            nameFirst="User",
            nameLast="Three",
            password="password123",
            privilege="USER",
            banned=False,
        ),
        User(
            username="user4",
            nameFirst="User",
            nameLast="Four",
            password="password123",
            privilege="USER",
            banned=False,
        ),
        User(
            username="user5",
            nameFirst="User",
            nameLast="Five",
            password="password123",
            privilege="USER",
            banned=False,
        ),
        User(
            username="user6",
            nameFirst="User",
            nameLast="Six",
            password="password123",
            privilege="USER",
            banned=False,
        ),
        User(
            username="user7",
            nameFirst="User",
            nameLast="Seven",
            password="password123",
            privilege="USER",
            banned=False,
        ),
        User(
            username="user8",
            nameFirst="User",
            nameLast="Eight",
            password="password123",
            privilege="USER",
            banned=False,
        ),
        User(
            username="user9",
            nameFirst="User",
            nameLast="Nine",
            password="password123",
            privilege="USER",
            banned=False,
        ),
        User(
            username="user10",
            nameFirst="User",
            nameLast="Ten",
            password="password123",
            privilege="USER",
            banned=False,
        ),
        User(
            username="user11",
            nameFirst="User",
            nameLast="Eleven",
            password="password123",
            privilege="USER",
            banned=False,
        ),
        User(
            username="user12",
            nameFirst="User",
            nameLast="Twelve",
            password="password123",
            privilege="USER",
            banned=False,
        ),
        User(
            username="user13",
            nameFirst="User",
            nameLast="Thirteen",
            password="password123",
            privilege="USER",
            banned=False,
        ),
        User(
            username="user14",
            nameFirst="User",
            nameLast="Fourteen",
            password="password123",
            privilege="USER",
            banned=False,
        ),
        User(
            username="user15",
            nameFirst="User",
            nameLast="Fifteen",
            password="password123",
            privilege="USER",
            banned=False,
        ),
        User(
            username="user16",
            nameFirst="User",
            nameLast="Sixteen",
            password="password123",
            privilege="USER",
            banned=False,
        ),
        User(
            username="user17",
            nameFirst="User",
            nameLast="Seventeen",
            password="password123",
            privilege="USER",
            banned=False,
        ),
        User(
            username="user18",
            nameFirst="User",
            nameLast="Eighteen",
            password="password123",
            privilege="USER",
            banned=False,
        ),
        User(
            username="user19",
            nameFirst="User",
            nameLast="Nineteen",
            password="password123",
            privilege="USER",
            banned=False,
        ),
        User(
            username="user20",
            nameFirst="User",
            nameLast="Twenty",
            password="password123",
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
