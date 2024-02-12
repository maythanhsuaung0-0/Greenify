function editField(input_change) {
  input_class = `#${input_change}-edit`;
  data_status = $(input_class).data("status");

  if (data_status == "on") {
    var new_input = $(`#${input_change}-input`).val().trim();
    var target_input = `#${input_change}`;

    if (new_input === "") {
      alert("Input cannot be empty.");
      return;
    } else if (input_change === 'name' || input_change === 'address') {
      const specialCharacterRegex = /^[a-zA-Z0-9\s]*$/;
      if (!specialCharacterRegex.test(new_input)) {
        alert("Special characters are not allowed.");
        return;
      }
    } else if (input_change === 'password' || input_change === 'confirm_password') {
      if (new_input.length < 8) {
        alert("Passwords must have at least 8 characters.");
        return;
      }
    } else if (input_change === 'contact_number') {
      if (new_input.length !== 8) {
        alert("Phone number must be 8 digits.");
        return;
      }
    } else if (input_change === 'postal_code') {
      if (new_input.length !== 6) {
        alert("Postal code must be 6 digits.");
        return;
      }
    }

    if (input_change === 'password' || input_change === 'confirm_password') {
      $(target_input).text(maskPassword(new_input)); // Update the target input with the masked password
    } else {
      $(target_input).text(new_input);
    }

    $(input_class).css('display', 'none');
    data_status = 'off';
  } else if (data_status == "off") {
    $(input_class).css('display', 'block');
    data_status = "on";
  }

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