#general formula we are using to calculcate priority of each assignment based on its attributes


urgent_window = 48.0 # 2 days
longer_task = 12.0  # hours for scaling L factor

def clamp(x, lo=0.0, hi=1.0): 
    return max(lo, min(hi, x))

def calculate_priority(due_date: float, longevity: float, value: int):
    slack = due_date - longevity
    T = clamp(1.0 - (slack / urgent_window))
    L = clamp((longevity) / longer_task)
    V = clamp((value-1) / 4.0)

    raw_result = (0.15 * T) + (0.55 * L) + (0.30 * V)
    raw_priority = raw_result
    priority = int(max(1, min(5, round(1 + 4*raw_result)))) # scale to 1-5

    return raw_priority, priority

#testing
#print(calculate_priority(24, 2, 2))  
#print(calculate_priority(160, 2, 2))  
#print(calculate_priority(10, 12, 5))  


