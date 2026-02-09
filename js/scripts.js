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
console.log("Looking for gallery container...");
var galleryContainer = document.querySelector(".gallery-section .scroll-container");
console.log("Gallery container found:", galleryContainer);

if (galleryContainer) {
  var scrollSpeed = 2; // pixels per frame - FASTER NOW (was 1)
  var scrollPosition = 0;
  var direction = 1; // 1 for right, -1 for left
  var isPaused = false;
  var isStarted = false;
  
  // Fade in images on load
  galleryContainer.style.opacity = 0;
  
  function autoScroll() {
    if (!isPaused && isStarted) {
      scrollPosition += scrollSpeed * direction;
      
      var maxScroll = galleryContainer.scrollWidth - galleryContainer.clientWidth;
      
      // Debug
      if (!window.debugLogged) {
        console.log("Scroll width:", galleryContainer.scrollWidth);
        console.log("Client width:", galleryContainer.clientWidth);
        console.log("Max scroll:", maxScroll);
        window.debugLogged = true;
      }
      
      // Reverse direction at ends
      if (scrollPosition >= maxScroll && direction === 1) {
        direction = -1;
        console.log("Reversing to left");
      } else if (scrollPosition <= 0 && direction === -1) {
        direction = 1;
        console.log("Reversing to right");
      }
      
      galleryContainer.scrollLeft = scrollPosition;
    }
    
    requestAnimationFrame(autoScroll);
  }
  
  // Start auto-scroll after images load
  window.addEventListener('load', function() {
    console.log("Page loaded, starting fade-in and auto-scroll...");
    
    // Fade in the gallery
    var opacity = 0;
    var fadeIn = setInterval(function() {
      if (opacity < 1) {
        opacity += 0.05;
        galleryContainer.style.opacity = opacity;
      } else {
        clearInterval(fadeIn);
        console.log("Fade-in complete");
      }
    }, 30);
    
    // Start scrolling after fade
    setTimeout(function() {
      isStarted = true;
      console.log("Auto-scroll started!");
      autoScroll();
    }, 800);
  });
  
  // Pause on hover
  galleryContainer.addEventListener('mouseenter', function() {
    console.log("Paused");
    isPaused = true;
  });
  
  galleryContainer.addEventListener('mouseleave', function() {
    console.log("Resumed");
    isPaused = false;
  });
} else {
  console.log("Gallery container not found!");
}
