// Save scroll position before page refresh
window.onbeforeunload = function () {
  localStorage.setItem("scrollPosition", window.scrollY);
};

// Restore scroll position on page load
window.onload = function () {
  var scrollPosition = localStorage.getItem("scrollPosition");
  if (scrollPosition !== null) {
    window.scrollTo(0, parseInt(scrollPosition));
    localStorage.removeItem("scrollPosition"); // Clear after restoration
  }
};
