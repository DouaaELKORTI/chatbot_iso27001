from flask import Flask, request, render_template, jsonify
from chatbot import ISO27001Chatbot
from conversational_handler import GestionnaireConversation, chat_ameliore
from pymongo import MongoClient

app = Flask(__name__)

# Connexion MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["chatbot_27001"]

# Initialisation du chatbot
chatbot = ISO27001Chatbot()

# Instance du gestionnaire de conversation
gestionnaire = GestionnaireConversation()

# Variable pour suivre si le message de bienvenue a été envoyé
bienvenue_envoye = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global bienvenue_envoye
    requete_utilisateur = request.json.get('message')
    if not requete_utilisateur:
        return jsonify({"error": "Aucun message fourni"}), 400
    
    reponse = chat_ameliore(requete_utilisateur, gestionnaire)
    # Ajouter le message de bienvenue uniquement pour la première requête
    if not bienvenue_envoye:
        reponse_json = reponse.get_json()
        reponse_json["response"] =  reponse_json["response"]
        reponse = jsonify(reponse_json)
        bienvenue_envoye = True

    if not gestionnaire.etape_actuelle or gestionnaire.etape_actuelle == "terminee":
        chatbot.log_query(requete_utilisateur, reponse.get_json()["response"], db)
    return reponse

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)