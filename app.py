from flask import Flask, request
import json
from codex2050_engine import handle_message

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json or {}
    chat = data.get('message', {}).get('chat', {})
    text = data.get('message', {}).get('text', '')
    response = handle_message(text)
    return {'ok': True, 'response': response}

@app.route('/')
def index():
    return "Codex2050 Super v1.3.4"
