from pymongo import MongoClient

def connect_db():
    """
    Connect to the MongoDB database.
    """
    client = MongoClient("mongodb://localhost:27017/")
    db = client["chatbot_iso27001"]
    return db
