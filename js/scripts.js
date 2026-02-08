// Interactive Archive Table
// Get all table rows within a table
var tableRows = document.querySelectorAll("table tbody tr");
var tableContainer = document.querySelector(".table-container");
var toggleButton = document.getElementById("toggleTable");

// Function to handle row click
function handleRowClick(row) {
  // Remove 'selected' class from all rows
  tableRows.forEach(function(row) {
    row.classList.remove('selected');
  });
  
  // Add 'selected' class to the clicked row
  row.classList.add('selected');
  
  // Get the value of the 'data-tab' attribute of the clicked row
  var projectId = row.getAttribute("data-tab");
  
  // Get the element with the corresponding id
  var targetElement = document.getElementById(projectId);
  
  if (!targetElement) return;
  
  // Hide all project content sections
  var allProjects = document.querySelectorAll(".project-content");
  allProjects.forEach(function(project) {
    project.style.display = "none";
  });
  
  // Show the target element
  targetElement.style.display = "flex";
  
  // Fade-in effect with opacity
  targetElement.style.opacity = 0;
  var fadeInInterval = setInterval(function() {
    if (targetElement.style.opacity < 1) {
      targetElement.style.opacity = parseFloat(targetElement.style.opacity) + 0.1;
    } else {
      clearInterval(fadeInInterval);
    }
  }, 50);
}

// Attach click event listener to each table row
tableRows.forEach(function(row) {
  row.addEventListener("click", function() {
    handleRowClick(this);
  });
});

// Display first project by default
window.addEventListener('DOMContentLoaded', (event) => {
  if (tableRows.length > 0) {
    handleRowClick(tableRows[0]); // Click first row by default
  }
});

// Toggle table collapse/expand
if (toggleButton) {
  toggleButton.addEventListener("click", function() {
    if (tableContainer.classList.contains("collapsed")) {
      // Expand
      tableContainer.classList.remove("collapsed");
      tableRows.forEach(function(row) {
        row.style.display = "";
      });
      toggleButton.textContent = "-";
    } else {
      // Collapse
      tableContainer.classList.add("collapsed");
      tableRows.forEach(function(row) {
        if (!row.classList.contains('selected')) {
          row.style.display = "none";
        }
      });
      toggleButton.textContent = "+";
    }
  });
}

// Gallery auto-scroll
var galleryContainer = document.querySelector(".gallery-section .scroll-container");
if (galleryContainer) {
  var scrollSpeed = 0.5; // pixels per frame
  var scrollPosition = 0;
  var maxScroll = galleryContainer.scrollWidth - galleryContainer.clientWidth;
  var direction = 1; // 1 for right, -1 for left
  
  function autoScroll() {
    scrollPosition += scrollSpeed * direction;
    
    // Reverse direction at ends
    if (scrollPosition >= maxScroll) {
      direction = -1;
    } else if (scrollPosition <= 0) {
      direction = 1;
    }
    
    galleryContainer.scrollLeft = scrollPosition;
    requestAnimationFrame(autoScroll);
  }
  
  autoScroll();
  
  // Pause on hover
  galleryContainer.addEventListener('mouseenter', function() {
    scrollSpeed = 0;
  });
  
  galleryContainer.addEventListener('mouseleave', function() {
    scrollSpeed = 0.5;
  });
}
