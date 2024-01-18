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
  if (creditCardValidation(credit_card_no)) {
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
}


