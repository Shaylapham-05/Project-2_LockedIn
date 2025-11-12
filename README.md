<H1> LockedIn - COP3530 - Project 2 </h1>
This is a tool to optimze your assignments based on your priorities.


<h2> Table of Contents </h2>

- [Overview](#overview)
- [Logic Overview](#logic-overview)
  - [Min-Heap](#min-heap)
  - [Priority Bucket](#priority-bucket)
- [Interactive Pages](#interavtive-pages)
  - [Calendar Page](#calendar-page)
  - [Dashboard Page](#dashboard-page)
  - [Analytics Page](#analytics-page)
- [Reflection](#reflection)
- [License](#license)

# Overview
Students frequently struggle with effective assignment prioritization.
LockedIn addresses this by automatically scheduling and visualizing academic tasks using two primary algorithms:
- Min-Heap
- Priority Bucket

Users can use the Dashboard, Calendar, and Analytics pages to visualize performance, schedule taskloads, and test scheduling techniques.

# Logic Overview
## Min-Heap

This sorts task by the earliest due date first. Most ideal for short term task management.
- Time complexity: **O(N log N)**

## Priority Bucket

This groups tasks by importance to the the students weight of the grade, then sorts within each bucket by due date. Most ideal for high value and long term tasks.
- Time complexity: **O(N log N)** (worst case)

# Interactive Pages:
## Calendar Page
The Calendar tab provides a monthly overview of all future assignments.

In which users can toggle tasks view based on:
- Priority
- Longevity
- Difficulty

## Dashboard Page
The Dashboard tab shows a daily breakdown of tasks. It provides current performance tasks and enables for sorting via toggle buttons:
- Priority
- Due Date
- Longevity
- Load New Tasks

Additionaly obtains a sidebar displaying different metrics:
- Tasks Completed
- Missed Deadlines
- Tasks Left
- Completion Rate (%)

## Analytics Page
The Analytics tab allows users to evaluate the performance of two algorithms: Min-Heap and Priority Bucket.

Users input:
- Time Window (hours)
- Workload (hours)

Displayed Metrics:
- **Execution Time** - how long the algorithm took in ms
- **Total Task** - all loaded assignements
- **Makespan** - total hours to complete all tasks
- **Tasks On Time** - number of tasks finshed before due date
- **Tasks Late** - number of taks finished after due date
- **On Time Rate** - percentage of tasks finished on time

# Reflection
We learned how to implement data structures and algorithms into real world wep apps. The comparison of heap based scheduling and bucket based scheduling demonstrated trade offs between performances and task value. 

# License
© 2025 LockedIn Team - Shayla Pham, Soni Reddy, Shreya Rajaram
