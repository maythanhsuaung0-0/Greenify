function editField(input_change) {
  input_class = `#${input_change}-edit`;
  data_status = $(input_class).data("status");

  if (data_status == "on") {
    // If the input field is visible (i.e., being edited)
    var new_input = $(`#${input_change}-input`).val().trim();
    var target_input = `#${input_change}`;

    if (new_input === "") {
      alert("Input cannot be empty.");
      return;
    } else if (input_change === 'name') {
      const specialCharacterRegex = /^[a-zA-Z0-9\s]*$/;
      if (!specialCharacterRegex.test(new_input)) {
        alert("Special characters are not allowed.");
        return;
      }
    } else if (input_change === 'address') {
      const specialCharacterRegex = /^[a-zA-Z0-9\s]*$/;
      if (!specialCharacterRegex.test(new_input)) {
        alert("Special characters are not allowed.");
        return;
      }
    }

    if (input_change === 'password' || input_change === 'confirm_password') {
            // If the input field is visible (i.e., being edited)
            $(target_input).text(maskPassword(new_input)); // Update the target input with the masked password
        } else {
            // For other fields, just update the target input with the new value
            $(target_input).text(new_input);
        }

    // Hide the input field
    $(input_class).css('display', 'none');
    data_status = 'off';
  } else if (data_status == "off") {
    // If the input field is hidden (i.e., not being edited)
    $(input_class).css('display', 'block');
    data_status = "on";
  }

  // Update the data status attribute
  $(input_class).data("status", data_status);
}

document.addEventListener("DOMContentLoaded", function() {
    var passwordSpan = document.getElementById("password");
    var password = passwordSpan.innerText;
    var maskedPassword = maskPassword(password);
    passwordSpan.innerText = maskedPassword;

    var confirmPasswordSpan = document.getElementById("confirm_password");
    var confirmPassword = confirmPasswordSpan.innerText;
    var maskedConfirmPassword = maskPassword(confirmPassword);
    confirmPasswordSpan.innerText = maskedConfirmPassword;
});

function maskPassword(password) {
    var masked = '';
    for (var i = 0; i < password.length; i++) {
        masked += '•';
    }
    return masked;
}