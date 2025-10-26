let theme = 'system';
if (localStorage.getItem('theme') === 'dark') {
  theme = 'dark';
} else if (localStorage.getItem('theme') === 'light') {
  theme = 'light';
}
setTheme(theme);

function setTheme(theme) {
  const html = document.querySelector('html');
  const chatRoot = document.getElementById('chat-root');
  if (theme === 'dark' || theme === 'light') {
    html.dataset.theme = theme;
    if (chatRoot) {
      chatRoot.dataset.theme = theme;
    }
    localStorage.setItem('theme', theme);
  } else {
    html.removeAttribute('data-theme');
    if (chatRoot) {
      chatRoot.removeAttribute('data-theme');
    }
    localStorage.removeItem('theme');
  }
  const toggle = document.querySelector('#theme-toggle');
  if (toggle) {
    toggle.querySelector('i').className = getIconClass(theme);
    toggle.setAttribute('aria-label', `Switch to ${nextTheme(theme)} mode`);
  }
}

function nextTheme(theme) {
  switch (theme) {
    case 'dark':
      return 'light';
    case 'light':
      return 'system';
    default:
      return 'dark';
  }
}

function getIconClass(theme) {
  switch (theme) {
    case 'dark':
      return 'fa-solid fa-moon';
    case 'light':
      return 'fa-regular fa-sun';
    default:
      return 'fa-solid fa-circle-half-stroke';
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.querySelector('#theme-toggle');
  if (toggle) {
    setTheme(theme);
    toggle.addEventListener('click', (e) => {
      e.preventDefault();
      theme = nextTheme(theme);
      setTheme(theme);
    });
  }
});
