const themeToggle = document.getElementById("themeToggle");
const root = document.documentElement;

function applyTheme(theme) {
  root.setAttribute("data-theme", theme);
  localStorage.setItem("theme", theme);
  if (themeToggle) {
    const icon = theme === "dark" ? "light_mode" : "dark_mode";
    const label = theme === "dark" ? "Light Mode" : "Dark Mode";
    themeToggle.innerHTML = `<span class="icon material-symbols-rounded" aria-hidden="true">${icon}</span>${label}`;
  }
}

const savedTheme = localStorage.getItem("theme");
if (savedTheme) {
  applyTheme(savedTheme);
} else {
  applyTheme("light");
}

if (themeToggle) {
  themeToggle.addEventListener("click", () => {
    const current = root.getAttribute("data-theme") || "dark";
    applyTheme(current === "dark" ? "light" : "dark");
  });
}
