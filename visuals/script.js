const themeToggle = document.getElementById('themeToggle');
const html = document.documentElement;
const themeIcon = document.querySelector('.theme-icon');

function setTheme(theme) {
  html.setAttribute('data-theme', theme);
  localStorage.setItem('theme', theme);
  themeIcon.textContent = theme === 'light' ? '🌙' : '☀️';
}

const savedTheme = localStorage.getItem('theme') || 'light';
setTheme(savedTheme);

themeToggle.addEventListener('click', () => {
  const currentTheme = html.getAttribute('data-theme');
  const newTheme = currentTheme === 'light' ? 'dark' : 'light';
  setTheme(newTheme);
});

let currentMode = 'priority';

document.querySelectorAll('.dropdown-content a').forEach(link => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    currentMode = e.target.getAttribute('data-mode');
    console.log(`Scheduling mode changed to: ${currentMode}`);
    document.querySelector('.dropdown-content').classList.remove('show');
  });
});

async function sendData() {
  const input = { 
    mode: currentMode,
    month: document.getElementById('month-name').textContent 
  };

  try {
    const response = await fetch("/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(input)
    });

    if (response.ok) {
      const result = await response.json();
      console.log("Backend result:", result);
      alert(`Algorithm executed with ${currentMode} mode!`);
    } else {
      console.error('Server error:', response.status);
      alert('Algorithm is ready to run with mode: ' + currentMode);
    }
  } catch (error) {
    console.log('Running in demo mode with settings:', input);
    alert(`Running scheduler with ${currentMode} mode for ${input.month}`);
  }
}

document.querySelector("#runBtn").addEventListener("click", sendData);
