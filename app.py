import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import requests
from translate import Translator

app = Flask(__name__)
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data['message']
    target_language = data['target_language']

    translator = Translator(to_lang='en')
    translated_user_message = translator.translate(user_message)

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [{"role": "user", "content": translated_user_message}],
        "temperature": 0.7,
        "max_tokens": 150
    }
    response = requests.post(GROQ_API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        ai_response = response.json()['choices'][0]['message']['content']
        
        translator = Translator(to_lang=target_language)
        translated_ai_response = translator.translate(ai_response)
        
        return jsonify({"response": translated_ai_response})
    else:
        return jsonify({"error": "Failed to get response from AI"}), 500

if __name__ == '__main__':
    app.run(debug=True)