#will calculate performance metrics for different scheduling algorithms
from typing import List, Tuple, Dict, Any
from assignment import Assignment

# schedule is a list of tuples: (Assignment, start_time, finish_time)
Schedule = List[Tuple[Assignment, float, float]]

def compute_metrics(schedule: Schedule, total_tasks_in: int) -> Dict[str, Any]:
    #analyzes a generated schedule and computes performance metrics.
    if not schedule:
        #default
        return {
            "total_lateness": 0.0,
            "tasks_on_time": 0,
            "tasks_late": 0,
            "on_time_rate": 1.0,
            "makespan": 0.0,
            "total_tasks": 0,
            "avg_priority": 0.0
        }

    total_lateness = 0.0
    tasks_on_time = 0
    tasks_late = 0
    total_raw_priority = 0.0
    total_tasks_scheduled = len(schedule)
    
    for task, start_time, finish_time in schedule:
        #lateness:how far past the due date the task finished.
        #if inished on time, lateness is 0 (not negative).
        lateness = max(0.0, finish_time - task.due_date)
        
        total_lateness += lateness
        
        if lateness > 0:
            tasks_late += 1
        else:
            tasks_on_time += 1
            total_raw_priority += task.raw_priority

    tasks_missed = total_tasks_in - total_tasks_scheduled    
            
    # makespan: finish time of the very last task in the schedule
    makespan = schedule[-1][2] if schedule else 0.0
    total_tasks = len(schedule)
    success_rate = (tasks_on_time / total_tasks_in) if total_tasks_in > 0 else 1.0

    avg_priority = (total_raw_priority / tasks_on_time) if total_tasks > 0 else 0.0
    
    return {
        "tasks_in_schedule": total_tasks_scheduled,
        "makespan": makespan,
        "avg_priority": avg_priority,
        "total_lateness": total_lateness,
        "tasks_on_time": tasks_on_time,
        "tasks_late": tasks_late,
        "tasks_missed": tasks_missed,  
        "success_rate": success_rate,
    }

    