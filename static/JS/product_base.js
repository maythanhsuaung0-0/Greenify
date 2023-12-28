var product_price = document.getElementById("price").innerText;
product_price = parseInt(product_price.slice(1));



function increment() {
    var product_qty = document.getElementById("qty-count").innerText;
    product_qty = parseInt(product_qty);
    product_qty += 1;
    document.getElementById("qty-count").innerText = product_qty;

    var product_price_update = product_qty * product_price;
    document.getElementById("price").innerText = '$' + product_price_update.toFixed(2);
}

function decrement() {
    var product_qty = document.getElementById("qty-count").innerText;
    product_qty = parseInt(product_qty);
    if (product_qty > 1) {
        product_qty -= 1;
        document.getElementById("qty-count").innerText = product_qty;

        var product_price_update = product_qty * product_price;
        document.getElementById("price").innerText = '$' + product_price_update.toFixed(2);
    }
}

