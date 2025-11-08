# Import core Flask modules
from flask import Flask, request, jsonify, send_from_directory
import pandas as pd  # used to load and handle tasks.csv
from src.scheduler import run_schedule  # step 1) import  algorithm function once ready
import os

# Initialize Flask app and set static folder for frontend files
app = Flask(__name__, static_folder='visuals', static_url_path='')

# Serve the frontend (index.html) when visiting the root URL
@app.route('/')
def serve_index():
    return send_from_directory('visuals', 'index.html')

# Define backend route for running algorithms
@app.route('/run', methods=['POST'])
def run_algorithm():
    # frontend sends data here 
    data = request.get_json()

    # Load your 100,000 simulated data points from tasks.csv
    df = pd.read_csv('data/tasks.csv')

    # call your algorithm logic here
    # step 2) result = run_schedule(df)  # pass dataset into your teammate’s function

    # For now, return placeholder response to confirm connection works
    result = {"status": "success", "received_data": data, "dataset_rows": len(df)}

    # return jsonify(result) returns result to frontend
    return jsonify(result)

# Start Flask server on port 81 (Replit default)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
