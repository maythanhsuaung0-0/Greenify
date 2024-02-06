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