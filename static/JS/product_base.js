function increment() {
    var product_qty = document.getElementById("qty-count").innerText;
    product_qty = parseInt(product_qty);
    product_qty += 1;
    document.getElementById("qty-count").innerText = product_qty;
}

function decrement() {
    var product_qty = document.getElementById("qty-count").innerText;
    product_qty = parseInt(product_qty);
    if (product_qty > 1) {
        product_qty -= 1;
        document.getElementById("qty-count").innerText = product_qty;
    }
}