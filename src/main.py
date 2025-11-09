import time
from typing import List
from assignment import Assignment
from scheduler_heap import schedule_minheap
from scheduler_bucket import schedule_from_buckets
from performance_metrics import compute_metrics
import random

def load_assignments(filename: str = "data/tasks.csv") -> List[Assignment]:
    #load assignments from csv
    assignments = []
    try:
        with open(filename, 'r') as f:
            next(f)  
            for line in f:
                try:
                    parts = line.strip().split(',')
                    # CSV has 5 columns: id, type, due_date, longevity, value
                    if len(parts) >= 5:
                        assignments.append(Assignment(
                            assignment_id=int(parts[0]),
                            assignment_type=parts[1],    
                            due_date=float(parts[2]),
                            longevity=float(parts[3]),
                            value=int(parts[4])
                            
                        ))
                    else:
                        print(f"Skipping malformed line: {line.strip()}")
                except ValueError as e:
                    print(f"Error parsing line: {line.strip()} - {e}")
                    
        print(f"Loaded {len(assignments)} total assignments.")
        
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
        return []
    except Exception as e:
        print(f"An error occurred while loading assignments: {e}")
        return []
        
    return assignments

def get_user_inputs():
    #user inputs times for window of assignments, and hours available to work
    try:
        time_window_str = input(f"Enter time window in hours (default to 1 week or 168 hours ): ")
        time_window = float(time_window_str) if time_window_str else 168.0
        
        workload_str = input(f"Enter realistic workload in hours (default: 60 hours): ")
        workload = float(workload_str) if workload_str else 60.0
        
        print(f"Running simulation with {workload:.1f}h workload in a {time_window:.1f}h window.\n")
        return time_window, workload
    except ValueError:
        print("Invalid input. Using default values (168.0, 60.0).")
        return 168.0, 60.0

def filter_and_sample_tasks(assignments: List[Assignment], time_window: float, workload: float) -> List[Assignment]:
    #filters tasks by due date and uses workload input
    
    #filter tasks that are due within the specified time window
    tasks_in_window = [a for a in assignments if a.due_date <= time_window]
    print(f"Found {len(tasks_in_window)} tasks due within {time_window:.1f} hours.")
    
    if not tasks_in_window:
        return []

    #shuffle the tasks to get a random mix
    random.shuffle(tasks_in_window)
    
    #sample tasks until we hit the desired workload
    student_tasks = []
    current_workload = 0.0
    for task in tasks_in_window:
        if current_workload + task.longevity <= workload:
            student_tasks.append(task)
            current_workload += task.longevity
        
    print(f"Simulating a single student's workload of {workload:.1f} hours...")
    print(f"Running schedulers on {len(student_tasks)} tasks (totaling {current_workload:.2f} hours).\n")
    return student_tasks

def print_comparison_table(metrics_heap, metrics_bucket):
    #prints a table comparing the two schedulers
    
    print("\n--- Scheduler Performance Comparison ---\n")
    
    print(f"{'Metric':<20} | {'Min-Heap (EDF)':<16} | {'Priority Bucket':<16}")
    print(f"{'-'*20:}|{'-'*16:}|{'-'*16:}")
    print(f"{'Execution Time (ms)':<20} | {metrics_heap['exec_time'] * 1000:<16.4f} | {metrics_bucket['exec_time'] * 1000:<16.4f}")
    print(f"{'Total Tasks In':<20} | {metrics_heap['total_tasks_in']:<16} | {metrics_bucket['total_tasks_in']:<16}")
    print(f"{'Tasks Scheduled':<20} | {metrics_heap['tasks_in_schedule']:<16} | {metrics_bucket['tasks_in_schedule']:<16}")
    print(f"{'Makespan (Total Hrs)':<20} | {metrics_heap['makespan']:<16.2f} | {metrics_bucket['makespan']:<16.2f}")
    print(f"{'Avg. Raw Priority':<20} | {metrics_heap['avg_priority']:<16.2f} | {metrics_bucket['avg_priority']:<16.2f}")
    print(f"{'Tasks On-Time':<20} | {metrics_heap['tasks_on_time']:<16} | {metrics_bucket['tasks_on_time']:<16}")
    print(f"{'Tasks Late':<20} | {metrics_heap['tasks_late']:<16} | {metrics_bucket['tasks_late']:<16}")
    print(f"{'Tasks Missed':<20} | {metrics_heap['tasks_missed']:<16} | {metrics_bucket['tasks_missed']:<16}")
    print(f"{'Success Rate (%)':<20} | {metrics_heap['success_rate'] * 100:<16.2f} | {metrics_bucket['success_rate'] * 100:<16.2f}")
    
    print("\n--- Analysis ---")
    
    #speed analysis
    if metrics_heap['exec_time'] < metrics_bucket['exec_time']:
        diff = metrics_bucket['exec_time'] - metrics_heap['exec_time']
        print(f"The Min-Heap (EDF) scheduler was FASTER by {diff * 1000:.4f} ms.")
    else:
        diff = metrics_heap['exec_time'] - metrics_bucket['exec_time']
        print(f"The Priority Bucket scheduler was FASTER by {diff * 1000:.4f} ms.")

    #missed task analysis
    if metrics_heap['tasks_missed'] < metrics_bucket['tasks_missed']:
        print(f"The Min-Heap (EDF) scheduler MISSED FEWER tasks.")
    elif metrics_bucket['tasks_missed'] < metrics_heap['tasks_missed']:
        print(f"The Priority Bucket scheduler MISSED FEWER tasks.")
    else:
        print(f"Both schedulers MISSED the same number of tasks.")

    #success rate comparison
    if metrics_heap['success_rate'] > metrics_bucket['success_rate']:
        print(f"The Min-Heap (EDF) scheduler had a BETTER success rate.")
    elif metrics_bucket['success_rate'] > metrics_heap['success_rate']:
        print(f"The Priority Bucket scheduler had a BETTER success rate.")
    else:
        print(f"Both schedulers had the SAME success rate.")
    
    print("-" * 58)

def main():
    print("--- Simulation Configuration ---")
    
    assignments = load_assignments()
    if not assignments:
        print("Exiting due to load error.")
        return

    time_window, workload = get_user_inputs()
    
    student_tasks = filter_and_sample_tasks(assignments, time_window, workload)
    
    if not student_tasks:
        print("No tasks found for the simulation. Exiting.")
        return
        
    total_tasks_in = len(student_tasks)

    # --- Run Min-Heap Scheduler ---
    print("Running Min-Heap (Earliest Deadline First) scheduler...")
    start_time = time.perf_counter()
    schedule_heap = schedule_minheap(student_tasks)
    end_time = time.perf_counter()
    exec_time_heap = end_time - start_time
    
    # --- Run Priority Bucket Scheduler ---
    print("Running Priority Bucket scheduler...")
    start_time = time.perf_counter()
    schedule_bucket = schedule_from_buckets(student_tasks)
    end_time = time.perf_counter()
    exec_time_bucket = end_time - start_time

    # --- Compute Metrics ---
    print("\nComputing metrics...")
    
    # --- UPDATED: Pass total_tasks_in to compute_metrics ---
    metrics_heap = compute_metrics(schedule_heap, total_tasks_in)
    metrics_heap['exec_time'] = exec_time_heap
    metrics_heap['total_tasks_in'] = total_tasks_in

    metrics_bucket = compute_metrics(schedule_bucket, total_tasks_in)
    metrics_bucket['exec_time'] = exec_time_bucket
    metrics_bucket['total_tasks_in'] = total_tasks_in
    
    # --- Print Results ---
    print_comparison_table(metrics_heap, metrics_bucket)
    
    print("\nProject execution complete.")

if __name__ == "__main__":
    main()