from flask import Flask, jsonify, send_from_directory
import os, sys, csv, time, random
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
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                assignments.append(Assignment(
                    assignment_id=int(row['assignment_id']),
                    assignment_type=row['assignment_type'],
                    due_date=float(row['due_date']),
                    longevity=float(row['longevity']),
                    value=int(row['value'])
                ))
            except (ValueError, TypeError):
                continue
    return assignments

def run_schedule(sample_size=25, time_window=168.0, workload=60.0):
    data_path = os.path.join("data", "tasks.csv")
    all_assignments = load_assignments(data_path)
    if not all_assignments:
        return {"status": "error", "message": "No data found."}

    tasks_in_window = [a for a in all_assignments if a.due_date <= time_window]
    random.shuffle(tasks_in_window)
    student_tasks, current_workload = [], 0.0
    for task in tasks_in_window:
        if current_workload + task.longevity <= workload:
            student_tasks.append(task)
            current_workload += task.longevity

    if not student_tasks:
        return {"status": "error", "message": "No tasks selected for scheduling."}

    total_tasks_in = len(student_tasks)

    start_heap = time.perf_counter()
    schedule_heap = schedule_minheap(student_tasks)
    exec_time_heap = time.perf_counter() - start_heap

    start_bucket = time.perf_counter()
    schedule_bucket = schedule_from_buckets(student_tasks)
    exec_time_bucket = time.perf_counter() - start_bucket

    metrics_heap = compute_metrics(schedule_heap, total_tasks_in)
    metrics_heap.update({
        "exec_time": exec_time_heap,
        "total_tasks_in": total_tasks_in
    })

    metrics_bucket = compute_metrics(schedule_bucket, total_tasks_in)
    metrics_bucket.update({
        "exec_time": exec_time_bucket,
        "total_tasks_in": total_tasks_in
    })

    return {
        "status": "success",
        "tasks_scheduled": len(student_tasks),
        "edf_time_ms": round(exec_time_heap * 1000, 3),
        "bucket_time_ms": round(exec_time_bucket * 1000, 3),
        "edf_metrics": metrics_heap,
        "bucket_metrics": metrics_bucket
    }

@app.route('/')
def serve_index():
    return send_from_directory('visuals', 'index.html')

@app.route('/dashboard')
def serve_dashboard():
    return send_from_directory('visuals', 'dashboard.html')

@app.route('/style.css')
def serve_css():
    return send_from_directory('visuals', 'style.css')

@app.route('/run', methods=['POST'])
def run_algorithm():
    result = run_schedule()
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
