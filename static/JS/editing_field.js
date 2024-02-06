function isFieldEmpty(input_change) {
    const field = document.getElementById(input_change);
    return field.value.trim() === '';
}

function editField(input_change) {
  input_class = `#${input_change}-edit`;
  data_status = $(input_class).data("status");
  if (data_status == "on") {
    $(input_class).css('display','none');
    data_status = 'off';

    var new_input = $(`#${input_change}-input`).val();
    var target_input = `#${input_change}`;
    $(target_input).text(new_input);

  } else if (data_status == "off") {
    $(input_class).css('display','block')
    data_status = "on"
  }

  $(input_class).data("status", data_status);
}

function validateEmail(email) {
            const re = /^[\w-]+(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]{2,7}$/;
            return re.test(String(email).toLowerCase());
        }

function validateEmailAndSubmit(input_change) {
    const input_class = `#${input_change}-edit`;
    const data_status = $(input_class).data("status");
    const emailInput = document.getElementById(input_change);
    const email = emailInput.value;

    if (!validateEmail(email)) {
        alert('Please enter a valid email address.');
        return; // Exit the function if email is invalid
    }

    // If email is valid, set data attribute accordingly
    $(input_class).data("status", data_status);
}

