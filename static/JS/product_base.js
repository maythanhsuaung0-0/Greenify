$("document").ready(function(){

    //Fetching Price of Product(Qty:1)
    var product_price = $("#price").text();
    product_price = parseInt(product_price.trim().slice(1));

    //Increment of Product
    $("#increment").click(function() {
        //Fetching Product Available Qty
        $.ajax({
            url: '',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                "request_type" : "product_stock",
            }),
            success: function(response) {
                var product_stock = response.stock
                var product_qty = $("#qty-count").text();
                product_qty = parseInt(product_qty);
                if (product_qty < product_stock) {
                    product_qty += 1;
                    $("#qty-count").text(product_qty);

                    var product_price_update = product_qty * product_price;
                    $("#price").text('$' + product_price_update.toFixed(2));
                }
            }
        })
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

    $.ajax({
            url: '',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
            "request_type" : "add_cart",
            "seller" : seller,
            "seller_id" : seller_id,
            "product_id" : product_id,
            "product_qty": product_qty
            }),
            success: function(response) {
            if (response.result) {
                $("#cart-item-qty").text(response.data)
            } else {
                if (response.reason == "added more than stock") {
                    alert("You have added more than the stock available");
                } else {
                    $(".content").text("FAIL");
                }
            }

            }
        })
}

//star rating
document.querySelector('.rating-wrapper').addEventListener('click', updateStarRating);

function updateStarRating(evt) {
  const stars = document.querySelectorAll('.rating-wrapper img');

  // Remove 'rating-checked' class from all stars
  stars.forEach(star => star.classList.remove('rating-checked'));

  // Add 'rating-checked' class to clicked star and previous stars
  const clickedStarIndex = parseInt(evt.target.id) - 1;
  for (let i = 0; i <= clickedStarIndex; i++) {
    stars[i].classList.add('rating-checked');
  }

  // Update the hidden input field with the selected rating
  document.querySelector('#rating').value = evt.target.id;
}