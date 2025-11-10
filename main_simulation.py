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
    #filters out tasks from tasks.csv that are due after the user inputted time window(time window is defined as the amount of time in hours from now that the user wants to see tasks for)
    tasks_in_window = [a for a in assignments if a.due_date <= time_window]

    target_sample_size = 25

    #if sample size is greater than or equal to 25, then randomly select ONLY 25 tasks from tasks.csv
    
    if len(tasks_in_window) >= target_sample_size:
        
        # if sampled 25 tasks fit the user input filter, randomly selects 25 of them.
        
        sampled_tasks = random.sample(tasks_in_window, target_sample_size)
        
    else:
        
        # if there are only less than 25 tasks available from tasks.csv that fit the user criteria, then use all available tasks  
        
        sampled_tasks = tasks_in_window

    #user inputs their worload limit - defined as the maximimum amount of time(in hours) they can spend on tasks in a week 
    student_tasks = []
    current_workload = 0.0

    #priority, longetivity, dificulty logic is implemented here for calendar webpage  
    sampled_tasks.sort(key=lambda t: t.due_date) 

    for t in sampled_tasks:
        # logic that filters objects from tasks.csv based on user inputted workload limit(amount of hours they can take on for a week) and ensures that the sum of the selected tasks longevity does not exceed the workload limit
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
        #collects 25 randomly displayed task object details from tasks.csv for frontend before displaying on analytics page 
        tasks_details = []
        for task in student_tasks:
            tasks_details.append({
                "id": task.assignment_id,
                "due": f"{task.due_date:.2f}",
                "length": f"{task.longevity:.2f}",
                "value": task.value
            })
        total_tasks_in = len(student_tasks)

        #print tasks to test algorithm logic and ensure tasks are being loaded correctly while integrating backend with frontend 
        print(f"\n Randomly Selected Tasks ({len(student_tasks)}) for Simulation:")
        for task in student_tasks:
            print(f"ID: {task.assignment_id}, Due: {task.due_date:.2f}, Length: {task.longevity:.2f}, Value: {task.value}")
        
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