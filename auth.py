import bcrypt
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

mongo_client = MongoClient(os.getenv("MONGO_URI"))
db = mongo_client["krishna_counsel"]

users_collection = db["users"]
history_collection = db["user_history"]


def register_user(username, password):
    if users_collection.find_one({"username": username}):
        return False, "User already exists"

    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    users_collection.insert_one({
        "username": username,
        "password": hashed_pw
    })

    history_collection.insert_one({
        "username": username,
        "questions": []
    })

    return True, "Registration successful"


def login_user(username, password):
    user = users_collection.find_one({"username": username})

    if not user:
        return False, "User not found"

    if bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        return True, "Login successful"

    return False, "Incorrect password"


def save_history(username, question, response):
    if username == "guest":
        return

    history_collection.update_one(
        {"username": username},
        {"$push": {
            "questions": {
                "question": question,
                "response": response
            }
        }}
    )