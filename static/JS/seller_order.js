function handleSendingOrder(orderIdHash,id) {
    console.log(orderIdHash, 'worked')
    var sent_out_container = document.getElementById("sent_out_container")
    var target_element =document.getElementById('card-'+orderIdHash)
    var send_out_length = document.getElementById("sent_out_length")
    var to_send_length = document.getElementById("to_send_length")
    console.log(sent_out_container)
    console.log(target_element)
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
           sent_out_container.appendChild(target_element)
           to_send_length.innerText = parseInt(to_send_length.innerText) - 1
            send_out_length.innerText = parseInt(to_send_length.innerText) + 1
            console.log(send_out_length,to_send_length)

           $('#card-'+orderIdHash).remove()
}
