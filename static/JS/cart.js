function increment(cart_item_id, product_price, seller_name, product_id) {
    //Update Qty Count
    var product_qty = $("#qty-count-" + cart_item_id).text();
    product_qty = parseInt(product_qty);
    product_qty += 1;
    $("#qty-count-" + cart_item_id).text(product_qty);

    //Update Indv Product Total Price
    var product_price_update = product_qty * product_price;
    $("#price-" + cart_item_id).text(product_price_update.toFixed(2));

    $.ajax({
        url: '',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            "request_type" : "update_cart_qty",
            "type" : "increment",
            "seller_name" : seller_name,
            "product_id" : product_id
        })
    })
    subtotal();
    total();
}

function decrement(cart_item_id, product_price, seller_name, product_id) {
    var product_qty = $("#qty-count-" + cart_item_id).text();
    product_qty = parseInt(product_qty);
    if (product_qty > 1) {
        product_qty -= 1;
        $("#qty-count-" + cart_item_id).text(product_qty);

        var product_price_update = product_qty * product_price;
        $("#price-" + cart_item_id).text(product_price_update.toFixed(2));

        $.ajax({
            url: '',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                "request_type" : "update_cart_qty",
                "type" : "decrement",
                "seller_name" : seller_name,
                "product_id" : product_id
            })
        })
        subtotal();
        total();
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
                subtotal();
                total();
            }
        }
    })
}

function subtotal() {
    var product_price_list = $(".indv-total-price").text().trim();
    product_price_list = product_price_list.slice(1).split('$');
    subtotal_price = 0
    for (var i = 0; i < product_price_list.length; i++) {
        price = product_price_list[i];
        price = parseFloat(price);

        subtotal_price += price;
    }

    $("#subtotal").text(subtotal_price.toFixed(2))
}

function total() {
    var subtotal = $("#subtotal").text().trim();
    subtotal = parseFloat(subtotal);

    var promo_price = $('#promo-price').text().trim();
    promo_price = parseFloat(promo_price);

    total_price = subtotal + 2 - promo_price;
    $('#total-price').text(total_price.toFixed(2));
}

function applyPromoCode() {
    var input_promo = $('#promo-code-input').val().toUpperCase();
    if (input_promo == "CNY2024") {
        promo_discount = 2
        $('#promo-price').text(promo_discount.toFixed(2));
        $('#promo-code-input').css('border-color', '#55aa65');
        try {
            $('#invalid-msg').remove();
        } catch{}
        total();
    } else {
        $('#promo-code-input').css('border-color', '#ff3b62');
        $('#promo-code-btn').after("<div id='invalid-msg'><p class='invalid'>Invalid Promo Code</p></div>")
    }
}

function checkout() {
    
}

subtotal();
total()
