document.addEventListener('DOMContentLoaded', () => {
  document.addEventListener('scroll', () => {
    document.querySelectorAll('.level').forEach((level) => {
      if (level.getBoundingClientRect().top <= window.innerHeight) {
        level.style.width = `${level.dataset.level * 10}%`;
      } else {
        level.style.width = '0%';
      }
    });
  });
});
