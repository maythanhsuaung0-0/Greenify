$(document).ready(function () {
  $(".datepicker").datepicker({
    format: "mm-yyyy",
    viewMode: "months",
    maxViewMode: "years",
    minViewMode: "months",
    orientation: "bottom",
    autoclose: true
  });
});

//Credit Card Checker
function creditCardValidation(creditCradNum) {
  var masterCard_regEx = /^5[1-5][0-9]{14}$|^2(?:2(?:2[1-9]|[3-9][0-9])|[3-6][0-9][0-9]|7(?:[01][0-9]|20))[0-9]{12}$/;
  var visa_regEx = /^4[0-9]{12}(?:[0-9]{3})?$/;
  if (creditCradNum.match(masterCard_regEx)) {
    return true;
  } else if (creditCradNum.match(visa_regEx)) {
    return true;
  } else {
    return false;
  }
}

//Pay
function payment() {
  var credit_card_no = $('#card-no').val();
  var cvv = $('#card-cvv').val();
  var date = $('#card-exp-date').val();


  if (cvv.length < 3) {
    $('#invalid-cvv').css('display', 'block');
  } else {
    $('#invalid-cvv').css('display', 'none');
  }
  if (date.match(/[\d]{2}\-[\d]{4}/)) {
    $('#invalid-exp-date').css('display', 'none');
  } else {
    $('#invalid-exp-date').css('display', 'block');
  }

  if (creditCardValidation(credit_card_no)) {
    $('#invalid-exp-date').css('display', 'none');

    var name = $('#name').text().trim();
    var email = $('#email').text().trim();
    var address = $('#address').text().trim();

    $.ajax({
      url: '',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({
        "request_type" : "payment",
        "name" : name,
        "email" : email,
        "address" : address
      }),
      success: function(response) {
        if (response.result) {
          window.location.href = response.redirect_link;
        }
      }
    })
  }
  else {
    $('#invalid-card').css('display', 'block')
  }

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