function togglePassword() {
    var passwordField = document.getElementById("password").querySelector("input");
    var eyeIcon = document.getElementById("eye-icon");

    if (passwordField.type === "password") {
      passwordField.type = "text";
      eyeIcon.className = "fa fa-eye-slash";
    } else {
      passwordField.type = "password";
      eyeIcon.className = "fa fa-eye";
    }
  }