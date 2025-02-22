from pymongo import MongoClient

def connect_db(mongo_uri="mongodb://localhost:27017/"):
    """Établir une connexion à la base de données MongoDB 'chatbot_27001'."""
    try:
        client = MongoClient(mongo_uri)
        db = client["chatbot_27001"]
        print("Connexion à MongoDB établie avec succès.")
        return db
    except Exception as e:
        print(f"Erreur lors de la connexion à MongoDB : {e}")
        raise