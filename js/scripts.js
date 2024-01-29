// Get all table rows within a table
var tableRows = document.querySelectorAll("table tr");

// Attach a click event listener to each table row
tableRows.forEach(function(row) {
  row.addEventListener("click", function() {

        
    // Get the value of the 'href' attribute of the clicked row
    var hrefValue = this.getAttribute("data-tab");

    // Get the element with the corresponding id
    var targetElement = document.getElementById(hrefValue);

    // Hide siblings and fade in the target element
    Array.from(targetElement.parentNode.children).forEach(function(sibling) {
      if (sibling !== targetElement) {
        sibling.style.display = "none";
      }
    });

    targetElement.style.display = "flex";
  
        // Assuming the target element should be displayed
    // Alternatively, you can use other methods to show the element, like adding a CSS class.
    // targetElement.classList.add("visible");

    // If you want a fadeIn effect, you can use CSS transitions or JavaScript animations
    // For simplicity, I'm using a simple fade-in effect with opacity
    targetElement.style.opacity = 0;
    var fadeInInterval = setInterval(function() {
      if (targetElement.style.opacity < 1) {
        targetElement.style.opacity = parseFloat(targetElement.style.opacity) + 0.1;
      } else {
        clearInterval(fadeInInterval);
      }
    }, 100);
  });
});
