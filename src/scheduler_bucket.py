from typing import List, Tuple, Dict
from assignment import Assignment

def build_buckets(assignments: List['Assignment']) -> Dict[int, List['Assignment']]:
# Create buckets for priorities 1 to 5 and sort assignments within each bucket
    buckets: Dict[int, List['Assignment']] = {i: [] for i in range(1, 6)}
    for a in assignments:
        if 1 <= a.priority <= 5:
            buckets[a.priority].append(a)
        else:
            pass
    for p in buckets:
        buckets[p].sort(key=lambda a: (
            a.due_date,      #1st: ascending due date (earliest first)
            -a.raw_priority, #2nd: descending raw priority (highest first- 5 (highest) to 1 (lowest))
            -a.longevity,    #3rd: descending longevity (longest first)
            -a.complexity    #4th: descending complexity (highest complex first)
            ))
    return buckets

def schedule_from_buckets(assignments: List['Assignment']) -> List[Tuple['Assignment', float, float]]:
# Schedule assignments from highest to lowest priority and iterate through pre-sorted list within each bucket
    buckets = build_buckets(assignments)
    clock = 0.0
    schedule: List[Tuple['Assignment', float, float]] = []
    for p in range(5, 0, -1):
        for a in buckets[p]:
            start_time = clock
            end_time = start_time + a.longevity
            schedule.append((a, start_time, end_time))
            clock = end_time
    return schedule
