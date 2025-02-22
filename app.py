from flask import Flask, request, render_template, jsonify
from chatbot import ISO27001Chatbot

app = Flask(__name__)
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
    chatbot.log_query(user_query, response)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)