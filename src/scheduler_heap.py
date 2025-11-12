from typing import List, Tuple
<<<<<<< HEAD
from src.minheap import MinHeap
from src.assignment import Assignment  # if your file is 'assignment.py', change this import
=======
from minheap import MinHeap
from assignment import Assignment  # if your file is 'assignment.py', change this import
>>>>>>> origin/shreya-data

def schedule_minheap(assignments: List[Assignment]) -> List[Tuple[Assignment, float, float]]:
    #orders by earliest due date, tie-break by higher raw_priority, then longer/harder.
    #returns list of (assignment, start_h, finish_h).

    key = lambda a: (a.due_date, -a.raw_priority, -a.longevity, -a.value)
    heap = MinHeap(key=key)
    for a in assignments:
        heap.push(a)

    clock = 0.0
    schedule: List[Tuple[Assignment, float, float]] = []
    while not heap.is_empty():
        a = heap.pop()
<<<<<<< HEAD
=======
        if a.due_date < clock:
            #give up and skip if due date passed
            continue
>>>>>>> origin/shreya-data
        start, finish = clock, clock + a.longevity
        clock = finish
        schedule.append((a, start, finish))
    return schedule
