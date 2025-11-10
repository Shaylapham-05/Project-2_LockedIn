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


def filter_and_sample_tasks(assignments: List[Assignment], time_window: float, workload: float) -> List[Assignment]:
    tasks_in_window = [a for a in assignments if a.due_date <= time_window]
    random.shuffle(tasks_in_window)
    student_tasks = []
    current_workload = 0.0
    for t in tasks_in_window:
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

        metrics_bucket = compute_metrics(schedule_bucket)
        metrics_bucket["exec_time"] = exec_time_bucket
        metrics_bucket["total_tasks_in"] = total_tasks_in

        return {"heap": metrics_heap, "bucket": metrics_bucket}

    except Exception as e:
        return {"error": str(e)}