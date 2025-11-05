import csv
import random
import os

# make sure folder exists
os.makedirs("data", exist_ok=True)

def generate_task(task_id):
    return {
        "assignment_id": task_id,
        "assignment_name": f"Assignment_{task_id}",
        "due_date": round(random.uniform(0, 168), 2),  # 0–167 hours (~7 days)
        "longevity": round(random.uniform(1, 6) * random.randint(1, 5), 2),
        "complexity": random.randint(1, 5),
        "priority": random.randint(1, 5)
    }

# generate 100,000 tasks
tasks = [generate_task(i) for i in range(1, 100001)]

# write to CSV
with open("data/tasks.csv", "w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["assignment_id", "assignment_name", "due_date", "longevity", "complexity", "priority"]
    )
    writer.writeheader()
    writer.writerows(tasks)

print("Dataset created at data/tasks.csv")