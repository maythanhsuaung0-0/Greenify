var logo = document.getElementById("mylogo");
var dashboard = document.getElementById("dashboard");
var business = document.getElementById("business");
var appForm = document.getElementById("appForm");
var updateForm = document.getElementById("updateForm");
var setting = document.getElementById("setting");

logo.addEventListener("click", function () {
    window.location.href = "/";
});

// Function to show active links in the sidebar
function showActiveNavLink() {
    // Get the current pathname
    var currentPathname = window.location.pathname;
    console.log(currentPathname)
    // Add active class to the nav link that corresponds to the current pathname
    if (currentPathname == "/staff/dashboard") { 
        dashboard.classList.add("active");
        // Remove active class from other elements
        business.classList.remove("active");
        appForm.classList.remove("active");
        updateForm.classList.remove("active");
        setting.classList.remove("active");
    }
    if (currentPathname == "/staff/retrieveSellers") {
        business.classList.add("active");
        // Remove active class from other elements
        dashboard.classList.remove("active");
        appForm.classList.remove("active");
        updateForm.classList.remove("active");
        setting.classList.remove("active");
    }
    if (currentPathname == "/staff/retrieveApplicationForms") { 
        appForm.classList.add("active");
        // Remove active class from other elements
        dashboard.classList.remove("active");
        business.classList.remove("active");
        updateForm.classList.remove("active");
        setting.classList.remove("active");
    }
    if (currentPathname == "/staff/retrieveUpdateForms") { 
        updateForm.classList.add("active");
        // Remove active class from other elements
        dashboard.classList.remove("active");
        business.classList.remove("active");
        appForm.classList.remove("active");
        setting.classList.remove("active");
    }
    if (currentPathname == "/staff/setting") { 
        setting.classList.add("active");
        // Remove active class from other elements
        dashboard.classList.remove("active");
        business.classList.remove("active");
        appForm.classList.remove("active");
        updateForm.classList.remove("active");
    }
}

// Attach the event listener for hash changes
window.addEventListener('hashchange', showActiveNavLink);

showActiveNavLink();



