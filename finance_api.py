# Description: Backend API using Python and Flask to upload and parse Excel files and store financial data

from flask import Flask, request, jsonify
# CORS allows the front-end app to call this API even if it's on a different server
from flask_cors import CORS
# secure_filename makes sure uploaded filenames are safe to save
from werkzeug.utils import secure_filename

import pandas as pd  # used to read Excel files easily
import mysql.connector
import os

UPLOAD_DIR = "uploads"          # folder to store uploaded files
ALLOWED_EXT = {"xlsx"}          # only allow Excel files

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_DIR
CORS(app)                        # enable cross-origin requests

# Make sure the uploads folder exists
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="dre",
    password="Live123",
    database="finance_db"
)
cursor = db.cursor(dictionary=True)  # return results as dictionaries for easy access

# Function to check if the uploaded file has a valid extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

# Endpoint to upload an Excel file for a specific user and year
@app.route("/api/finances/upload/<int:user_id>/<int:year>", methods=["POST"])
def upload_file(user_id, year):
    # check if the post request has a file
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']

    # if no file is selected
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # check the file extension
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type, only .xlsx files are allowed'}), 400

    # secure the filename and save it
    safe_filename = secure_filename(file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
    file.save(path)

    # read Excel data and save to database
    try:
        df = pd.read_excel(path)
        df.columns = df.columns.str.strip().str.capitalize()  # normalize column names

        # loop through each row and insert into the financial_records table
        for index, row in df.iterrows():
            month = row['Month']
            amount = row['Amount']
            cursor.execute(
                "INSERT INTO financial_records (user_id, year, month, amount) VALUES (%s, %s, %s, %s)",
                (user_id, year, month, amount)
            )
        db.commit()
    except Exception as e:
        return jsonify({"error": f"Error reading Excel file: {str(e)}"}), 500

    return jsonify({"message": "File has been uploaded and data has been saved"}), 201

# Endpoint to fetch all financial records for a specific user and year
@app.route("/api/finances/<int:user_id>/<int:year>", methods=["GET"])
def fetch_records(user_id, year):
    cursor.execute(
        "SELECT month, amount FROM financial_records WHERE user_id=%s AND year=%s",
        (user_id, year)
    )
    records = cursor.fetchall()
    return jsonify(records), 200

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
