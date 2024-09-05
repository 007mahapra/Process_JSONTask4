from flask import Flask, request, jsonify , send_from_directory
from pymongo import MongoClient
import requests
import re
# Maha : TO allow CORS sharing otherwise index.html can not access the endpoints
from flask_cors import CORS

app = Flask(__name__)

# Initialize CORS
CORS(app)

# Connect to MongoDB database
client = MongoClient("mongodb://mongo:27017/")
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
