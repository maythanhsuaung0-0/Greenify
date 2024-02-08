function handleButton(id,name,action) {
    console.log(id, name, 'worked')
    var id_to_handle = parseInt(id);
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

function filter(filter_by){
console.log(filter_by)
$.ajax({
             url: '',
             type: 'POST',
             contentType: 'application/json',
             data: JSON.stringify({
                 "request_type": "filter",
                 "filter_by":filter_by,
             }),
             success: function (response) {
                 // Handle success if needed
                 if(response.result){
                 console.log(response.result,"filtered successful");
                 alert('Successfully '+ action+'d '+name)}
             },
             error: function (xhr, status, error) {
                 // Handle error if needed
                 console.error("Error:", error);
             }
         });
}
