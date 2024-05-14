// Get all table rows within a table
var tableRows = document.querySelectorAll("table tr");

// Function to handle row click
function handleRowClick(row) {
  // Remove 'selected' class from all rows
  tableRows.forEach(function(row) {
    row.classList.remove('selected');
  });

  // Add 'selected' class to the clicked row
  row.classList.add('selected');

  // Get the value of the 'data-tab' attribute of the clicked row
  var hrefValue = row.getAttribute("data-tab");

  // Get the element with the corresponding id
  var targetElement = document.getElementById(hrefValue);

  // Hide siblings and fade in the target element
  Array.from(targetElement.parentNode.children).forEach(function(sibling) {
    if (sibling !== targetElement) {
      sibling.style.display = "none";
    }
  });
  targetElement.style.display = "flex";

  // Fade-in effect with opacity
  targetElement.style.opacity = 0;
  var fadeInInterval = setInterval(function() {
    if (targetElement.style.opacity < 1) {
      targetElement.style.opacity = parseFloat(targetElement.style.opacity) + 0.1;
    } else {
      clearInterval(fadeInInterval);
    }
  }, 100);
}

// Attach click event listener to each table row
tableRows.forEach(function(row) {
  row.addEventListener("click", function() {
    handleRowClick(this);
  });
});

// Display one data tab by default
window.addEventListener('DOMContentLoaded', (event) => {
  var defaultRow = document.querySelector("table tr.push");
  if (defaultRow) {
    handleRowClick(defaultRow);
  }
});
