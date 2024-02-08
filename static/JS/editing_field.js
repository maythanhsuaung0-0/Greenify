function editField(input_change) {
  input_class = `#${input_change}-edit`;
  data_status = $(input_class).data("status");

  if (data_status == "on") {
    // If the input field is visible (i.e., being edited)
    var new_input = $(`#${input_change}-input`).val().trim();
    var target_input = `#${input_change}`;

    if (new_input === "") {
      // If the input is empty, show an alert and prevent further action
      alert("Input cannot be empty.");
      return;
    } else if (input_change === 'email') { // If the input is for email
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(new_input)) {
        // If the input is not a valid email, show an alert and prevent further action
        alert("Please enter a valid email address.");
        return;
      }
    }

    // If the input is not empty or if it's an email and it's valid, update the target input with the new value
    $(target_input).text(new_input);

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