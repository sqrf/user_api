import os
from config import db
from models.user import User

# Data to initialize database with

USERS = [
    {"email": "sqrf@gmail.com", "password": "hiro123", "full_name": "Rafael Silva"},
    {"email": "superman@gmail.com", "password": "steel123", "full_name": "Clark Kent"},
]


def init_database():
    # Delete database file if it exists currently
    if os.path.exists("users.db"):
        os.remove("users.db")

    # Create the database
    db.create_all()

    # iterate over the USERS structure and populate the database
    for user in USERS:
        p = User(email=user.get("email"), password=user.get("password"), full_name=user.get("full_name"))
        db.session.add(p)

    db.session.commit()
