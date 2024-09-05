# Ransomware API To interact with [Ransomware Database](https://raw.githubusercontent.com/codingo/Ransomware-Json-Dataset/master/ransomware_overview.json)

This project helps to get the Ransomeware JSON from [github link](https://raw.githubusercontent.com/codingo/Ransomware-Json-Dataset/master/ransomware_overview.json) and helps to store it in database.
It uses the Mongo as database 
This README provides an overview of the available API endpoints for managing ransomware data. The API allows you to load, create, retrieve, update, and delete ransomware records stored in a MongoDB database. The endpoints are accessible through standard HTTP methods.

## Tech Stack

- **Python**: Python is the primary programming language used for building the API. I have used Flask from Python to create the API.
- **MongoDB**: MongoDB is used as the data structure is not fixed and the json records don't have fix scema. The API connects to a MongoDB instance to interact with the ransomware data.
- **HTML and JavaScript** : The frontend of the API is built using HTML and JavaScript.


## Prerequisites
This project can be executed on any machine with the following prerequisites:

- Python 3.x
   - Libraries: Flask, pymongo  [Python Required Libraries](requirements.txt)
- MongoDB installed and running

But for the ease of use I have used docker to run the project. Here are the steps to run the project using Docker:

Note : Docker should be installed on your machine and docker-compose should be installed.

## Installation steps

1. Clone the repository:

```bash 
git clone https://github.com/007mahapra/Process_JSONTask4.git
```
2. Navigate to the project directory: Ransomware-API-Docker
3. Run the Docker image: 
   ```bash
   docker-compose up --build
   ```
4. Access the API at http://localhost:5000
5. This project also has frontend which can be accessed at http://localhost:5000 and the frontend is built using HTML and JavaScript.
6. The frontend is already configured to use the API endpoints, so you can interact with the API directly from the frontend and perform various operations.



## Front End documentation
The frontend is built using HTML and JavaScript. It has basic HTML, CSS, and JavaScript code to display the ransomware records and perform CRUD operations. 

I have used JavaScript to make the API calls to the backend API and use [Datatables](https://datatables.net/) library to display the data. The Front end allows to search, sort, and filter the data. It also has a search bar to search for ransomware records.

You can download the data in csv & excel. (PDF, Print format can also be enabled by making some changes in the datatable code)

Front end can be accessed at http://localhost:5000 

Guide is uploaded here for the frontend. [Front End Guide & Peroformed steps](guide_steps)


## API Endpoints to interact with the API and perform basic CRUD operations

### 1. Load JSON Data into MongoDB

- **Endpoint**: `/load_json`
- **Method**: `POST`
- **Description**: Loads ransomware data from a predefined JSON dataset into the MongoDB database. It uses an upsert operation to avoid duplicates based on the `name` field.
- **Usage**: 
  ```bash
  curl -X POST http://localhost:5000/load_json
  ```
- **Response**:
  - `201 Created`: Data loaded successfully.

### 2. Create a New Ransomware Record

- **Endpoint**: `/ransomware`
- **Method**: `POST`
- **Description**: Adds a new ransomware record to the MongoDB collection.
- **Usage**:
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"name": "Sample Ransomware", "encryptionAlgorithm": "AES"}' http://localhost:5000/ransomware
  ```
- **Response**:
  - `201 Created`: Record added successfully.

### 3. Retrieve All Ransomware Records

- **Endpoint**: `/ransomware`
- **Method**: `GET`
- **Description**: Retrieves all ransomware records from the database.
- **Usage**:
  ```bash
  curl -X GET http://localhost:5000/ransomware
  ```
- **Response**:
  - `200 OK`: Returns a JSON array of all ransomware records.

### 4. Retrieve a Single Ransomware Record by Name

- **Endpoint**: `/ransomware/<name>`
- **Method**: `GET`
- **Description**: Retrieves a specific ransomware record by its `name`.
- **Usage**:
  ```bash
  curl -X GET http://localhost:5000/ransomware/<name>
  ```
- **Response**:
  - `200 OK`: Returns the ransomware record in JSON format.
  - `404 Not Found`: Record not found.

### 5. Update a Ransomware Record by Name

- **Endpoint**: `/ransomware/<name>`
- **Method**: `PUT`
- **Description**: Updates an existing ransomware record by its `name`.
- **Usage**:
  ```bash
  curl -X PUT -H "Content-Type: application/json" -d '{"encryptionAlgorithm": "RSA"}' http://localhost:5000/ransomware/<name>
  ```
- **Response**:
  - `200 OK`: Record updated successfully.
  - `404 Not Found`: Record not found.

  Note : You can update any field of the record. You can also pass the whole json object to update the record.
```bash
  -d '{
  "name": ["ExampleRansom"],
  "extensions": ".example",
  "ransomNoteFilenames": "READ_ME.txt",
  "encryptionAlgorithm": "AES-256",
  "resources": ["http://example.com/resource"],
  "microsoftDetectionName": "Trojan:Win32/Example",
  "microsoftInfo": "https://www.microsoft.com/security/portal/threat/example",
  "sandbox": "https://www.hybrid-analysis.com/sample/example",
  "iocs": "https://otx.alienvault.com/pulse/example",
  "snort": "alert tcp any any -> any any (msg:\"Example snort rule\";)"
}```

### 6. Delete a Ransomware Record by Name

- **Endpoint**: `/ransomware/<name>`
- **Method**: `DELETE`
- **Description**: Deletes a specific ransomware record by its `name`.
- **Usage**:
  ```bash
  curl -X DELETE http://localhost:5000/ransomware/<name>
  ```
- **Response**:
  - `200 OK`: Record deleted successfully.
  - `404 Not Found`: Record not found.


## Want to run the project locally ?

To run the Flask application, use the following command:

```bash
python app.py
```

The application will be accessible at `http://localhost:5000`.

## References
Datatables : https://datatables.net/
Mongodb : https://www.mongodb.com/
https://blog.logrocket.com/build-deploy-flask-app-using-docker/

