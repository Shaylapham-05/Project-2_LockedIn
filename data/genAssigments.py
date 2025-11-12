import csv
import random
import os

# make sure folder exists
os.makedirs("data", exist_ok=True)

#types of assignments
ASSIGNMENT_TYPES = [
    "Study for test",
    "Essay",
    "Math problems",
    "Lab report",
    "Project",
    "Reading",
    "Research paper",
    "Coding assignment",
    "Presentation",
    "Discussion post"
]

def generate_task(task_id):
    longevity = round(random.uniform(1, 6) * random.randint(1, 5), 2)
    value = random.randint(1, 5)
    
    # spread tasks over 100 years 
    hours_in_100_years = 100 * 52 * 168
    due_date = round(random.uniform(24, hours_in_100_years), 2) 
   
    
    #ensure due_date is always after longevity
    due_date = max(due_date, longevity + 2.0) #2 hours of buffer
    
    return {
        "assignment_id": task_id,
        "assignment_type": random.choice(ASSIGNMENT_TYPES),
        "due_date": due_date,
        "longevity": longevity,
        "value": value
    }

# generate 100,000 tasks
tasks = [generate_task(i) for i in range(1, 100001)]

# write to CSV
with open("data/tasks.csv", "w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["assignment_id", "assignment_type", "due_date", "longevity", "value"]
    )
    writer.writeheader()
    writer.writerows(tasks)

print("Dataset created at data/tasks.csv")