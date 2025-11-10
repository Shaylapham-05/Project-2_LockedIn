async function runScheduler(mode) {
  const input = {
    mode,
    time_window: parseFloat(document.querySelector("#timeWindow").value) || 168,
    workload: parseFloat(document.querySelector("#workload").value) || 60
  };
  try {
    const response = await fetch("/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(input)
    });
    
    const result = await response.json();
    if (result.error) {
      alert("Error: " + result.error);
      return;
      
    }

    
    document.getElementById("execTime").textContent = `${(result.exec_time * 1000).toFixed(2) ?? '-'} ms`;
    document.getElementById("totalTasks").textContent = result.total_tasks ?? "-";
    document.getElementById("makespan").textContent = `${result.makespan.toFixed(2) ?? '-'} hrs`;
    document.getElementById("tasksOnTime").textContent = result.tasks_on_time ?? "-";
    document.getElementById("tasksLate").textContent = result.tasks_late ?? "-";
    document.getElementById("onTimeRate").textContent = `${(result.on_time_rate * 100).toFixed(0) ?? 0}%`;
  } catch (err) 
  {
    alert("Backend not responding.");
  }
  
}

document.querySelector("#runHeap").addEventListener("click", () => runScheduler("heap"));
document.querySelector("#runBucket").addEventListener("click", () => runScheduler("bucket"));
