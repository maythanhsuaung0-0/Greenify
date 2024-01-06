function increment(cart_item_id, product_price, seller_name, product_id) {
    //Update Qty Count
    var product_qty = $("#qty-count-" + cart_item_id).text();
    product_qty = parseInt(product_qty);
    product_qty += 1;
    $("#qty-count-" + cart_item_id).text(product_qty);

    //Update Indv Product Total Price
    var product_price_update = product_qty * product_price;
    $("#price-" + cart_item_id).text(product_price_update.toFixed(2));

    //Update Cart Icon Qty
    var cart_qty = $('#cart-item-qty').text().trim();
    cart_qty = parseInt(cart_qty);
    cart_qty += 1;
    $('#cart-item-qty').text(cart_qty);
    $.ajax({
        url: '',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            "request_type" : "update_cart_qty",
            "type" : "increment",
            "seller_name" : seller_name,
            "product_id" : product_id,
            "product_qty" : product_qty,
            "cart_qty" : cart_qty
        })
    })
}

function decrement(cart_item_id, product_price, seller_name, product_id) {
    var product_qty = $("#qty-count-" + cart_item_id).text();
    product_qty = parseInt(product_qty);
    if (product_qty > 1) {
        product_qty -= 1;
        $("#qty-count-" + cart_item_id).text(product_qty);

        var product_price_update = product_qty * product_price;
        $("#price-" + cart_item_id).text(product_price_update.toFixed(2));

        //Update Cart Icon Qty
        var cart_qty = $('#cart-item-qty').text().trim();
        cart_qty = parseInt(cart_qty);
        cart_qty -= 1;
        $('#cart-item-qty').text(cart_qty);
        $.ajax({
            url: '',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                "request_type" : "update_cart_qty",
                "type" : "decrement",
                "seller_name" : seller_name,
                "product_id" : product_id,
                "product_qty" : product_qty,
                "cart_qty" : cart_qty
            })
        })
    }
}

function removeProduct(cart_item_id, seller_name, product_id) {

    $.ajax({
        url: '',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            "request_type" : "delete_product",
            "seller_name" : seller_name,
            "product_id" : product_id
        }),
        success: function(response) {
            if (response.result) {
                $('#product-' + cart_item_id).remove()
                if (response.cart_qty != 0) {
                    $('#cart-item-qty').text(response.cart_qty);
                }
                else {
                    document.getElementById("content-body").innerHTML = `<h1>Your Shopping Cart is Empty</h1>`;

                }
            }
        }
    })
}

function subtotal() {
    var product_price_list = $(".indv-total-price").text().trim();
    console.log(product_price_list);
}

subtotal();