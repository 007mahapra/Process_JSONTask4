from flask import Flask, request, jsonify , send_from_directory
from pymongo import MongoClient
import os
import requests
import re
# Maha : TO allow CORS sharing otherwise index.html can not access the endpoints
from flask_cors import CORS

app = Flask(__name__)

# Initialize CORS
CORS(app)

# Connect to MongoDB database
# Use Railway-provided MongoDB URI if available, otherwise fall back to local mongo service
mongo_uri = (
    os.environ.get("MONGO_URL") or
    os.environ.get("MONGO_PRIVATE_URL") or   # Railway internal network
    os.environ.get("MONGO_PUBLIC_URL") or    # Railway public URL
    os.environ.get("DATABASE_URL") or
    os.environ.get("LOCAL_DATABASE_URL")
)
if not mongo_uri:
    raise ValueError("MongoDB connection string is not set in environment variables.")
else:
    if mongo_uri and "authSource" not in mongo_uri:
       mongo_uri += ("&" if "?" in mongo_uri else "?") + "authSource=admin"
    print(f"Using MongoDB URI: {mongo_uri}")
client = MongoClient(mongo_uri+ "/ransomware_db")
db = client.ransomware_db
collection = db.ransomware_collection

# Function to load JSON data into MongoDB
def load_json_to_db():
    url = "https://raw.githubusercontent.com/codingo/Ransomware-Json-Dataset/master/ransomware_overview.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for record in data:
            # Maha: Using upsert to avoid duplicates based on unique 'name' field
            collection.update_one(
                {"name": record.get("name")},
                {"$set": record},
                upsert=True
            )


# Serve index.html for testing functionality from web page for SCB to test the endpoints
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


# Usage        : API to trigger JSON load
# Method       : POST
@app.route('/load_json', methods=['POST'])
def load_json():
    load_json_to_db()
    return jsonify({"message": "Data loaded successfully"}), 201


# Usage        : API to create a new record
# Method       : POST
@app.route('/ransomware', methods=['POST'])
def create_ransomware():
    data = request.json
    collection.insert_one(data)
    return jsonify({"message": "Record added successfully"}), 201

# Usage        : API to retrieve records
@app.route('/ransomware', methods=['GET'])
def get_all_ransomware():
    records = list(collection.find({}, {"_id": 0}))
    return jsonify(records), 200

# Usage        : API to retrieve a single record by name
@app.route('/ransomware/<name>', methods=['GET'])
def get_ransomware(name):
    record = collection.find_one({"name": name}, {"_id": 0})
    if record:
        return jsonify(record), 200
    return jsonify({"message": "Record not found"}), 404

# Usage        :  API to update a record by name
@app.route('/ransomware/<name>', methods=['PUT'])
def update_ransomware(name):
    data = request.json
    result = collection.update_one({"name": name}, {"$set": data})
    if result.matched_count:
        return jsonify({"message": "Record updated successfully"}), 200
    return jsonify({"message": "Record not found"}), 404

# Usage        : API to delete a record by name
@app.route('/ransomware/<name>', methods=['DELETE'])
def delete_ransomware(name):
    result = collection.delete_one({"name": name})
    if result.deleted_count:
        return jsonify({"message": "Record deleted successfully"}), 200
    return jsonify({"message": "Record not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
