from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import os

app = Flask(__name__, static_folder='visuals', static_url_path='')

@app.route('/')
def serve_index():
    return send_from_directory('visuals', 'index.html')
    
@app.route('/dashboard')
def serve_dashboard():
    path = os.path.join(app.static_folder, 'dashboard.html')
    print("Serving dashboard from:", path)
    return send_from_directory(app.static_folder, 'dashboard.html')


@app.route('/run', methods=['POST'])
def run_algorithm():
    # receive frontend data
    data = request.get_json()

    # placeholder since algorithm isn’t implemented yet
    df = pd.DataFrame({"placeholder": [1, 2, 3]})
    result = {"status": "success", "received_data": data, "dataset_rows": len(df)}

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
