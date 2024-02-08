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

//function validateEmail(email) {
//            const re = /^[\w-]+(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]{2,7}$/;
//            return re.test(String(email).toLowerCase());
//        }

function getEmailInput() {
    const emailInput = document.getElementById('email-input');
    const email = emailInput.value;
    return email;
}

//function validateEmailAndSubmit(input_change) {
//    const input_class = `#${input_change}-edit`;
//    const data_status = $(input_class).data("status");
//    const emailInput = $(`#${input_change}-input`);
//    const email = emailInput.text();
//
//    if (validateEmail(email) == false) {
//        alert('Please enter a valid email address.');
//        return; // Exit the function if email is invalid
//    } else {
//        editField('email')
//    }
//}

function validateEmailAndSubmit(fieldId) {
    const email = getEmailInput();
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (emailRegex.test(email)) {
        // Save the email information here
        console.log('Valid email:', email);
        // Hide the edit field and show the email
        const emailElement = document.getElementById('email');
        emailElement.textContent = email;
        const hiddenField = document.getElementById(fieldId + '-edit');
        hiddenField.style.display = 'none';
    } else {
        alert('Please enter a valid email address.');
    }
}
