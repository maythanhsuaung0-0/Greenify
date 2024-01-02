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
})

function addToCart(product_id, seller_id, seller) {
    var product_qty = $("#qty-count").text();
    product_qty = parseInt(product_qty.trim());
    var cart_item_qty = $("#cart-item-qty").text().trim();
    cart_item_qty = parseInt(cart_item_qty);
    cart_item_qty += 1;
    $.ajax({
            url: '',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
            "seller" : seller,
            "seller_id" : seller_id,
            "product_id" : product_id,
            "product_qty": product_qty,
            "cart_item_qty" : cart_item_qty
            }),
            success: function(response) {
            if (response.result) {
                localStorage.setItem("cart_qty", response.data)
                $("#cart-item-qty").text(response.data)
            } else {
                $(".content").text("FAIL")
            }

            }
        })
}
