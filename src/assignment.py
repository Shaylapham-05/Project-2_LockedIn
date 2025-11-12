from dataclasses import dataclass
<<<<<<< HEAD
from src.priority import calculate_priority
=======
from priority import calculate_priority
>>>>>>> origin/shreya-data

@dataclass
class Assignment:
    #characteristics of each assignment
    assignment_id: int
    assignment_type: str
    due_date: float       # hours until deadline
    longevity: float      # est hours to complete
    value: int       # 1–5
    raw_priority: float = 0.0
    priority: int = 1

    def __post_init__(self):
        # compute priority at construction
        self.raw_priority, self.priority = calculate_priority(
            self.due_date, self.longevity, self.value
        )