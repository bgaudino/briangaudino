document.addEventListener('DOMContentLoaded', () => {
  document.addEventListener('scroll', fillBars);
  document.addEventListener('htmx:afterSwap', function (e) {
    if (e.detail.pathInfo?.responsePath === '/resume/') {
      fillBars();
    }
  });
  fillBars(); // Initial call to set the widths on page load
});

function fillBars() {
  document.querySelectorAll('.level').forEach((level) => {
    if (level.getBoundingClientRect().top <= window.innerHeight) {
      level.style.width = `${level.dataset.level * 10}%`;
    } else {
      level.style.width = '0%';
    }
  });
}
