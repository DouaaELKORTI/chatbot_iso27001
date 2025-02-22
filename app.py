from flask import Flask, request, render_template, jsonify
from chatbot import ISO27001Chatbot
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["chatbot_27001"]  # Base de données 'chatbot_27001'

# Initialize chatbot
chatbot = ISO27001Chatbot()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_query = request.json.get('message')
    if not user_query:
        return jsonify({"error": "Aucun message fourni"}), 400
    
    response = chatbot.get_response(user_query)
    # Pass the MongoDB database instance to log_query
    chatbot.log_query(user_query, response, db)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)