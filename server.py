from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app) # Allows our HTML file to talk to this Python server

DB_FILE = 'database.json'

# Create the database file if it doesn't exist
if not os.path.exists(DB_FILE):
    with open(DB_FILE, 'w') as f:
        json.dump({"users": [], "leaderboard": []}, f)

def load_db():
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    db = load_db()
    
    # Check if user already exists
    for user in db['users']:
        if user['username'] == data['username'] or user['mobile'] == data['mobile']:
            return jsonify({"success": False, "message": "User or Mobile already exists"}), 400
            
    db['users'].append({"mobile": data['mobile'], "username": data['username'], "password": data['password']})
    save_db(db)
    return jsonify({"success": True, "message": "Registration successful!"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    db = load_db()
    
    for user in db['users']:
        if user['username'] == data['username'] and user['password'] == data['password']:
            return jsonify({"success": True, "username": user['username']})
            
    return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route('/score', methods=['POST'])
def save_score():
    data = request.json
    db = load_db()
    
    db['leaderboard'].append({"user": data['username'], "score": data['score']})
    # Sort by highest score and keep top 10
    db['leaderboard'] = sorted(db['leaderboard'], key=lambda x: x['score'], reverse=True)[:10]
    
    save_db(db)
    return jsonify({"success": True})

@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    db = load_db()
    return jsonify(db['leaderboard'])

if __name__ == '__main__':
    print("🚀 Game Server running on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)