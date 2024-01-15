function handleButton(id,name,action) {
    console.log(id, name, 'worked')
    var opt_to_handle = confirm(`Are you sure you want to ${action} ${name}?`);
    var id_to_handle = parseInt(id);
     if (opt_to_handle) {
         $.ajax({
             url: '',
             type: 'POST',
             contentType: 'application/json',
             data: JSON.stringify({
                 "request_type": action,
                 "id": id_to_handle,
             }),
             success: function (response) {
                 // Handle success if needed
                 if(response.result){
                 console.log(response.result,"Delete successful");
                 alert('Successfully '+ action+'d '+name)}
             },
             error: function (xhr, status, error) {
                 // Handle error if needed
                 console.error("Error:", error);
             }
         });
           $('#card-'+id).remove()
     }

}
