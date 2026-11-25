// MediCare Hub – Premium UI Script

document.addEventListener('DOMContentLoaded', function () {

  // 1. Auto-dismiss alerts
  document.querySelectorAll('.alert-dismissible').forEach(function (el) {
    setTimeout(function () {
      const a = new bootstrap.Alert(el);
      if (a) a.close();
    }, 5500);
  });

  // 2. Tooltips
  document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(function (el) {
    new bootstrap.Tooltip(el, { trigger: 'hover' });
  });

  // 3. Active nav link highlight
  const currentPath = window.location.pathname;
  document.querySelectorAll('.navbar-nav .nav-link').forEach(function (link) {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active-link');
    }
  });

  // 4. Animate rows on scroll (IntersectionObserver)
  const observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.animate-in').forEach(function (el) {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.45s ease, transform 0.45s ease';
    observer.observe(el);
  });

  // 5. Smooth progress-bar animation
  document.querySelectorAll('.progress-bar').forEach(function (bar) {
    const target = bar.style.width;
    bar.style.width = '0%';
    bar.style.transition = 'width 0.9s cubic-bezier(.25,.46,.45,.94)';
    requestAnimationFrame(function () {
      setTimeout(function () { bar.style.width = target; }, 150);
    });
  });

});
