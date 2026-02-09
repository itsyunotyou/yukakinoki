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
  var opacity = 0;
  var fadeIn = setInterval(function() {
    if (opacity < 1) {
      opacity += 0.1;
      targetElement.style.opacity = opacity;
    } else {
      clearInterval(fadeIn);
    }
  }, 30);
  
  // Start auto-scroll for this project
  startProjectAutoScroll(targetElement);
}

// Auto-scroll for archive project images
function startProjectAutoScroll(projectElement) {
  var scrollContainer = projectElement.querySelector('.scroll-container');
  if (!scrollContainer) return;
  
  var scrollSpeed = 2;
  var scrollPosition = 0;
  var direction = 1;
  var isPaused = false;
  
  // Stop any existing animation
  if (scrollContainer.autoScrollRunning) {
    scrollContainer.autoScrollRunning = false;
  }
  
  scrollContainer.autoScrollRunning = true;
  
  function autoScroll() {
    if (!scrollContainer.autoScrollRunning) return;
    
    if (!isPaused) {
      scrollPosition += scrollSpeed * direction;
      
      var maxScroll = scrollContainer.scrollWidth - scrollContainer.clientWidth;
      
      // Reverse direction at ends
      if (scrollPosition >= maxScroll && direction === 1) {
        direction = -1;
      } else if (scrollPosition <= 0 && direction === -1) {
        direction = 1;
      }
      
      scrollContainer.scrollLeft = scrollPosition;
    }
    
    requestAnimationFrame(autoScroll);
  }
  
  autoScroll();
  
  // Pause on hover
  scrollContainer.addEventListener('mouseenter', function() {
    isPaused = true;
  });
  
  scrollContainer.addEventListener('mouseleave', function() {
    isPaused = false;
  });
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
  var scrollSpeed = 2;
  var scrollPosition = 0;
  var direction = 1;
  var isPaused = false;
  var isStarted = false;
  
  // Fade in images on load
  galleryContainer.style.opacity = 0;
  
  function autoScroll() {
    if (!isPaused && isStarted) {
      scrollPosition += scrollSpeed * direction;
      
      var maxScroll = galleryContainer.scrollWidth - galleryContainer.clientWidth;
      
      // Reverse direction at ends
      if (scrollPosition >= maxScroll && direction === 1) {
        direction = -1;
      } else if (scrollPosition <= 0 && direction === -1) {
        direction = 1;
      }
      
      galleryContainer.scrollLeft = scrollPosition;
    }
    
    requestAnimationFrame(autoScroll);
  }
  
  // Start after page loads and images fade in
  window.addEventListener('load', function() {
    // Fade in the gallery
    var opacity = 0;
    var fadeIn = setInterval(function() {
      if (opacity < 1) {
        opacity += 0.05;
        galleryContainer.style.opacity = opacity;
      } else {
        clearInterval(fadeIn);
      }
    }, 30);
    
    // Start scrolling after short delay
    setTimeout(function() {
      isStarted = true;
      autoScroll();
    }, 800);
  });
  
  // Pause on hover
  galleryContainer.addEventListener('mouseenter', function() {
    isPaused = true;
  });
  
  galleryContainer.addEventListener('mouseleave', function() {
    isPaused = false;
  });
}
