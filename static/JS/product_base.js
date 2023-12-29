$("document").ready(function(){

    //Fetching Price of Product(Qty:1)
    var product_price = $("#price").text();
    product_price = parseInt(product_price.trim().slice(1));

    //Increment of Product
    $("#increment").click(function() {
        var product_qty = $("#qty-count").text();
        product_qty = parseInt(product_qty);
        product_qty += 1;
        $("#qty-count").text(product_qty);

        var product_price_update = product_qty * product_price;
        $("#price").text('$' + product_price_update.toFixed(2));
    })

    //Decrement of Product
    $("#decrement").click(function() {
        var product_qty = $("#qty-count").text();
        product_qty = parseInt(product_qty);
        if (product_qty > 1) {
            product_qty -= 1;
            $("#qty-count").text(product_qty);

            var product_price_update = product_qty * product_price;
            $("#price").text('$' + product_price_update.toFixed(2));
        }
    })

    $("#addCart").click(function(){
        var product_qty = $("#qty-count").text();
        product_qty = parseInt(product_qty.trim());
        $.ajax({
            url: '',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
            "product": product,
            "product_qty": product_qty
            })
        })
    })



})
