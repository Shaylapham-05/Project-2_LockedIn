async function sendData() {
  const input = { task1: "Example", task2: "Test" }; // Replace with your form data

  const response = await fetch("/run", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input)
  });

  const result = await response.json();
  console.log("Backend result:", result);
}

// Example trigger:
document.querySelector("#runBtn").addEventListener("click", sendData);
