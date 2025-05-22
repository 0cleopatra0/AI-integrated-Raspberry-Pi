import json
from flask import Flask, request, jsonify
from pymongo import MongoClient
import requests
from dotenv import load_dotenv
from threading import Thread
# Load environment variables from .env
load_dotenv()
OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'phi3:mini')
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
MAX_HISTORY = 2
CONFIG_FILE = 'config.json'
app = Flask(__name__)
client = MongoClient(MONGO_URI)
db = client['rpi_llm_db']
users_collection = db['users']
qa_collection = db['qa_history']
# Health check
try:
    client.admin.command('ping')
    print("MongoDB connection: SUCCESS")
except Exception as e:
    print(" MongoDB connection ERROR:", e)
# Pre-warm model in background
def warmup_model():
    try:
        print("Warming up the model...")
        _ = requests.post(f"{OLLAMA_HOST}/api/generate", json={
            "model": OLLAMA_MODEL,
            "prompt": "Hello",
            "num_predict": 1,
            "stream": False
        }, timeout=600)
        print("Model is warmed up.")
    except Exception as e:
        print("Model warmup failed:", e)
Thread(target=warmup_model).start()
# Load user config if exists
def load_user_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}
def save_user_config(user_id, intellect):
    with open(CONFIG_FILE, 'w') as f:
        json.dump({"user_id": user_id, "intellect": intellect}, f)
@app.route('/')
def index():
    return jsonify({"message": "Raspberry Pi LLM API is running."})
@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json(force=True, silent=True) or {}
    user_id = data.get('user_id')
    question = data.get('question')
    if not user_id or not question:
        return jsonify({'error': 'user_id and question are required'}), 400
    user = users_collection.find_one({'user_id': user_id})
    if not user:
        return jsonify({'error': 'User not found. Please set intellect level.'}), 404
    intellect = user.get('intellect', 'normal')
    
    # Get last N Q&A history
    history = list(qa_collection.find({"user_id": user_id})
                   .sort("timestamp", -1).limit(MAX_HISTORY))
    context = ""
    for h in reversed(history):
        context += f"Q: {h['question']}\nA: {h['answer']}\n"
    # Add instruction based on intellect level
    if intellect == 'high':
        instruction = "Explain this in a detailed and complex manner:"
    elif intellect == 'low':
        instruction = "Explain this simply and clearly:"
    else:
        instruction = "Answer this question:"
    prompt = f"{context}\n{instruction} {question}"
    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "num_predict": 100,
                "stream": False
            }, timeout=600
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Model request failed: {e}'}), 500
    answer = response.json().get('response', 'Sorry, no response.')
    # Avoid saving duplicate question-answer
    if not qa_collection.find_one({'user_id': user_id, 'question': question}):
        qa_collection.insert_one({
           'user_id': user_id,
            'question': question,
            'answer': answer,
            'intellect_level': intellect,
            'timestamp': datetime.now(timezone.utc)
        })
    return jsonify({
        'user_id': user_id,
        'intellect_level': intellect,
        'question': question,
        'answer': answer
    })
@app.route('/user/<user_id>', methods=['PUT'])
def set_user_intellect(user_id):
    data = request.get_json(force=True, silent=True) or {}
    intellect = data.get('intellect', 'normal').lower()
    if intellect not in {'low', 'normal', 'high'}:
        return jsonify({'error': 'Intellect must be "low", "normal", or "high".'}), 400
    users_collection.update_one(
        {'user_id': user_id},
        {'$set': {'intellect': intellect}},
        upsert=True
    )
    save_user_config(user_id, intellect)
    return jsonify({'user_id': user_id, 'intellect': intellect})
@app.route('/reset/<user_id>', methods=['DELETE'])
def reset_user_data(user_id):
    users_collection.delete_one({'user_id': user_id})
    qa_collection.delete_many({'user_id': user_id})
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
    return jsonify({'message': f'User {user_id} data cleared.'})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=FLASK_PORT, debug=False)


