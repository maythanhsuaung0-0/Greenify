function togglePasswordVisibility(passwordInputId, eyeIconClass) {
    var passwordInput = document.getElementById(passwordInputId);
    var eyeIcon = document.querySelector(eyeIconClass);

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        eyeIcon.classList.remove("fa-eye");
        eyeIcon.classList.add("fa-eye-slash");
    } else {
        passwordInput.type = "password";
        eyeIcon.classList.remove("fa-eye-slash");
        eyeIcon.classList.add("fa-eye");
    }
}
