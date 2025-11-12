import time
import random
from typing import List
from src.assignment import Assignment
from src.scheduler_heap import schedule_minheap
from src.scheduler_bucket import schedule_from_buckets
from src.performance_metrics import compute_metrics


def load_assignments(filename: str = "data/tasks.csv") -> List[Assignment]:
    assignments = []
    try:
        with open(filename, 'r') as f:
            next(f)
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 5:
                    assignments.append(
                        Assignment(
                            assignment_id=int(parts[0]),
                            assignment_type=parts[1],
                            due_date=float(parts[2]),
                            longevity=float(parts[3]),
                            value=int(parts[4])
                        )
                    )
        print(f"Loaded {len(assignments)} total assignments.")
        return assignments
    except FileNotFoundError:
        print(f"Error: File not found -> {filename}")
        return []


def filter_and_sample_tasks(assignments: List[Assignment], time_window: float, workload: float, sort_mode: str) -> List[Assignment]:
 
    tasks_in_window = [a for a in assignments if a.due_date <= time_window]

    target_sample_size = 25

 
    if len(tasks_in_window) >= target_sample_size:
        tasks_in_window.sort(key=lambda t: t.due_date)
        sampled_tasks = tasks_in_window[:target_sample_size]
    else:
        sampled_tasks = tasks_in_window

   
    if sort_mode == 'priority':
        sort_key = lambda t: t.due_date
        sampled_tasks.sort(key=sort_key)
    elif sort_mode == 'longevity':
        sort_key = lambda t: t.longevity
        sampled_tasks.sort(key=sort_key)
    elif sort_mode == 'difficulty':
        sort_key = lambda t: t.value
        sampled_tasks.sort(key=sort_key, reverse=True)

   
    student_tasks = []
    current_workload = 0.0

    for t in sampled_tasks:
        if current_workload + t.longevity <= workload:
            student_tasks.append(t)
            current_workload += t.longevity

    return student_tasks


def run_simulation(time_window: float, workload: float):
    try:
        assignments = load_assignments("data/tasks.csv")
        if not assignments:
            return {"error": "No assignments loaded"}

        student_tasks = filter_and_sample_tasks(assignments, time_window, workload) 

      
        tasks_details = []
        for task in student_tasks:
            tasks_details.append({
                "id": task.assignment_id,
                "due": f"{task.due_date:.2f}",
                "length": f"{task.longevity:.2f}",
                "value": task.value,
                "assignment_type": task.assignment_type
            })
        total_tasks_in = len(student_tasks)

        start_heap = time.perf_counter()
        schedule_heap = schedule_minheap(student_tasks)
        exec_time_heap = time.perf_counter() - start_heap

        start_bucket = time.perf_counter()
        schedule_bucket = schedule_from_buckets(student_tasks)
        exec_time_bucket = time.perf_counter() - start_bucket

        
        metrics_heap = compute_metrics(schedule_heap)
        metrics_heap["exec_time"] = exec_time_heap
        metrics_heap["total_tasks_in"] = total_tasks_in
        metrics_heap["tasks_list"] = tasks_details

        metrics_bucket = compute_metrics(schedule_bucket)
        metrics_bucket["exec_time"] = exec_time_bucket
        metrics_bucket["total_tasks_in"] = total_tasks_in
        metrics_bucket["tasks_list"] = tasks_details

        return {"heap": metrics_heap, "bucket": metrics_bucket}

    except Exception as e:
        
        return {"error": str(e)}