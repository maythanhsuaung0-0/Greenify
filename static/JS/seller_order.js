function handleSendingOrder(orderIdHash,id) {
    console.log(orderIdHash, 'worked')
    var id_to_handle = parseInt(id);
         $.ajax({
             url: '',
             type: 'POST',
             contentType: 'application/json',
             data: JSON.stringify({
                 "request_type": 'order_sent',
                 "id": orderIdHash,
             })
         });
//           $('#card-'+id).remove()

}
