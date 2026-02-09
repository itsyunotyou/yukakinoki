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

// Gallery auto-scroll - START IMMEDIATELY
console.log("=== GALLERY AUTO-SCROLL DEBUG ===");
var galleryContainer = document.querySelector(".gallery-section .scroll-container");
console.log("1. Gallery container found:", galleryContainer);

if (galleryContainer) {
  console.log("2. Container exists, checking dimensions...");
  console.log("   scrollWidth:", galleryContainer.scrollWidth);
  console.log("   clientWidth:", galleryContainer.clientWidth);
  
  var scrollSpeed = 2;
  var scrollPosition = 0;
  var direction = 1;
  var isPaused = false;
  
  // Fade in images
  galleryContainer.style.opacity = 0;
  var opacity = 0;
  var fadeIn = setInterval(function() {
    if (opacity < 1) {
      opacity += 0.05;
      galleryContainer.style.opacity = opacity;
    } else {
      clearInterval(fadeIn);
      console.log("3. Fade-in complete");
    }
  }, 30);
  
  function autoScroll() {
    if (!isPaused) {
      scrollPosition += scrollSpeed * direction;
      
      var maxScroll = galleryContainer.scrollWidth - galleryContainer.clientWidth;
      
      // Reverse direction at ends
      if (scrollPosition >= maxScroll && direction === 1) {
        direction = -1;
        console.log("   Reversing to LEFT");
      } else if (scrollPosition <= 0 && direction === -1) {
        direction = 1;
        console.log("   Reversing to RIGHT");
      }
      
      galleryContainer.scrollLeft = scrollPosition;
    }
    
    requestAnimationFrame(autoScroll);
  }
  
  // Start immediately
  console.log("4. Starting auto-scroll NOW");
  setTimeout(function() {
    console.log("5. AUTO-SCROLL STARTED!");
    autoScroll();
  }, 800);
  
  // Pause on hover
  galleryContainer.addEventListener('mouseenter', function() {
    console.log("   Scroll PAUSED");
    isPaused = true;
  });
  
  galleryContainer.addEventListener('mouseleave', function() {
    console.log("   Scroll RESUMED");
    isPaused = false;
  });
} else {
  console.log("ERROR: Gallery container NOT FOUND!");
}
