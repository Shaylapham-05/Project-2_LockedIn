from flask import Flask, request, jsonify, send_from_directory
from main_simulation import run_simulation
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VISUALS_DIR = os.path.join(BASE_DIR, "visuals")

app = Flask(__name__, static_folder=VISUALS_DIR, static_url_path="")

@app.route("/")
def serve_index():
    return send_from_directory(VISUALS_DIR, "index.html")

@app.route("/dashboard")
def serve_dashboard():
    return send_from_directory(VISUALS_DIR, "dashboard.html")


@app.route("/analytics")
def serve_analytics():
    return send_from_directory(VISUALS_DIR, "analytics.html")

@app.route("/run", methods=["POST"])
def run_algorithm():
    data = request.get_json()


    time_window = float(data.get("time_window", 168))
    workload = float(data.get("workload", 60))
    mode = data.get("mode", "heap")
    sort_mode = data.get("sort_mode", "priority") 

   
    results = run_simulation(time_window, workload) 


    if "error" in results:
        return jsonify(results)

    return jsonify(results.get(mode, {}))


if __name__ == '__main__':
    print(f"Serving Flask from: {VISUALS_DIR}")
    app.run(host='0.0.0.0', port=0, debug=True)