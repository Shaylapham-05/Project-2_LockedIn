#will calculate performance metrics for different scheduling algorithms
from typing import List, Tuple, Dict, Any
from assignment import Assignment

# schedule is a list of tuples: (Assignment, start_time, finish_time)
Schedule = List[Tuple[Assignment, float, float]]

def compute_metrics(schedule: Schedule) -> Dict[str, Any]:
    #analyzes a generated schedule and computes performance metrics.
    if not schedule:
        #default
        return {
            "total_lateness": 0.0,
            "tasks_on_time": 0,
            "tasks_late": 0,
            "on_time_rate": 1.0,
            "makespan": 0.0,
            "total_tasks": 0
        }

    total_lateness = 0.0
    tasks_on_time = 0
    tasks_late = 0
    
    for task, start_time, finish_time in schedule:
        #lateness:how far past the due date the task finished.
        #if inished on time, lateness is 0 (not negative).
        lateness = max(0.0, finish_time - task.due_date)
        
        total_lateness += lateness
        
        if lateness > 0:
            tasks_late += 1
        else:
            tasks_on_time += 1
            
    # makespan: finish time of the very last task in the schedule
    makespan = schedule[-1][2] if schedule else 0.0
    total_tasks = len(schedule)
    on_time_rate = (tasks_on_time / total_tasks) if total_tasks > 0 else 1.0
    
    return {
        "total_lateness": total_lateness,
        "tasks_on_time": tasks_on_time,
        "tasks_late": tasks_late,
        "on_time_rate": on_time_rate,
        "makespan": makespan,
        "total_tasks": total_tasks
    }