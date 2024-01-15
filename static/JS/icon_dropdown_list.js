// Function to toggle the dropdown
    function toggleDropdown() {
      var dropdown = document.getElementById("myDropdown");
      dropdown.style.display = (dropdown.style.display === "block") ? "none" : "block";
    }

    // Close the dropdown if the user clicks outside of it
    window.onclick = function(event) {
      if (!event.target.matches('.bi-person-circle')) {
        var dropdown = document.getElementById("myDropdown");
        if (dropdown.style.display === "block") {
          dropdown.style.display = "none";
        }
      }
    }