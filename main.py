
from flask import Flask, jsonify, send_from_directory
import os
import sys
import csv
import time
import random
from typing import List


sys.path.append(os.path.join(os.path.dirname(__file__), "src"))


from assignment import Assignment
from scheduler_heap import schedule_minheap
from scheduler_bucket import schedule_from_buckets
from performance_metrics import compute_metrics


app = Flask(__name__)



def load_assignments(filepath: str) -> List[Assignment]:
    assignments = []
    if not os.path.exists(filepath):
        print(f"[ERROR] File not found: {filepath}")
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                a = Assignment(
                    assignment_id=int(row['assignment_id']),
                    assignment_type=row['assignment_type'],
                    due_date=float(row['due_date']),
                    longevity=float(row['longevity']),
                    value=int(row['value'])
                )
                assignments.append(a)
            except (ValueError, TypeError):
                continue
    return assignments



def run_schedule(sample_size=25):
    data_path = os.path.join("data", "tasks.csv")
    all_assignments = load_assignments(data_path)
    if not all_assignments:
        return {"status": "error", "message": "No data found."}

    #randomly sampled 25 tasks from the dataset
    sampled = random.sample(all_assignments, sample_size)

    # Convert from hours to days by /24 , starting at April 6 on calendar 
    for a in sampled:
        a.due_date /= 24
        a.longevity /= 24

   
    start_heap = time.perf_counter()
    schedule_heap = schedule_minheap(sampled)
    heap_time = (time.perf_counter() - start_heap) * 1000

    start_bucket = time.perf_counter()
    schedule_bucket = schedule_from_buckets(sampled)
    bucket_time = (time.perf_counter() - start_bucket) * 1000

    # metrics computed here 
    metrics_heap = compute_metrics(schedule_heap)
    metrics_bucket = compute_metrics(schedule_bucket)

    return {
        "status": "success",
        "tasks_scheduled": len(sampled),
        "edf_time_ms": round(heap_time, 3),
        "bucket_time_ms": round(bucket_time, 3),
        "edf_metrics": metrics_heap,
        "bucket_metrics": metrics_bucket
    }


#app routes listed here 
@app.route('/')
def serve_index():
    return send_from_directory('visuals', 'index.html')
    

@app.route('/dashboard')
def serve_dashboard():
    visuals_path = os.path.join(os.path.dirname(__file__), 'visuals')
    print("DEBUG visuals path:", visuals_path)
    print("DEBUG files:", os.listdir(visuals_path))
    return send_from_directory(visuals_path, 'dashboard.html')



@app.route('/style.css')
def serve_css():
    return send_from_directory('visuals', 'style.css')


@app.route('/run', methods=['POST'])
def run_algorithm():
    result = run_schedule()
    return jsonify(result)


#make sure port is correct here 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
