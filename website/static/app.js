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

// no enter on search box + listen on F5
document.addEventListener('DOMContentLoaded', function () {
  var searchForm = document.getElementById('search-form');
  var searchBox = document.getElementById('search-box');

  // Load the search term from localStorage on page load
  var savedSearch = localStorage.getItem('searchTerm');
  if (savedSearch) {
    searchBox.value = savedSearch;
    search();
  }

  searchForm.addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent form submission
    search();
  });
});

function updateSearch() {
  var searchBox = document.getElementById('search-box');
  var searchTerm = searchBox.value;

  // Save the search term to localStorage
  localStorage.setItem('searchTerm', searchTerm);
}

function search() {
  var searchBox = document.getElementById('search-box');
  var searchText = searchBox.value.toLowerCase();
  var rows = document.querySelectorAll('table tr');

  rows.forEach(function (row) {
    var cells = row.querySelectorAll('td');
    var found = false;

    cells.forEach(function (cell) {
      var cellText = cell.textContent.toLowerCase();

      if (cellText.includes(searchText)) {
        found = true;
      }
    });

    if (found) {
      row.style.display = 'table-row';
    } else {
      row.style.display = 'none';
    }
  });
}

