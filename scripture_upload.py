import os
import json
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["krishna_counsel"]

collection = db["scriptures"]   # ONE universal collection


def upload_scriptures():
    data_folder = "data"

    if not os.path.exists(data_folder):
        print("❌ 'data' folder not found.")
        return

    for file in os.listdir(data_folder):

        if file.endswith(".json"):
            file_path = os.path.join(data_folder, file)

            print(f"📖 Uploading {file}...")

            with open(file_path, "r", encoding="utf-8") as f:
                verses = json.load(f)

            scripture_name = file.replace(".json", "").capitalize()

            for verse in verses:
                verse["scripture"] = scripture_name

            collection.insert_many(verses)

            print(f"✅ {file} uploaded successfully!")

    print("\n🎉 All scriptures uploaded!")


if __name__ == "__main__":
    upload_scriptures()