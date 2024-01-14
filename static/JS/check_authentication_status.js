function route() {
    document.getElementById('redirectLink').addEventListener('click', function(event) {
    }
        event.preventDefault(); // Prevent the default link behavior

        // Check login status via AJAX
        fetch('/check_login')
            .then(response => response.json())
            .then(loggedIn => {
                const redirectUrl = loggedIn ? this.getAttribute('data-profile') : this.getAttribute('data-login');
                window.location.href = redirectUrl; // Redirect based on the login status and link attribute
            })
            .catch(error => console.error('Error:', error));
    });
}