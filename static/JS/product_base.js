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

// Fetch initial reviews
//function fetchInitialReviews(seller_id, product_id) {
//    $.ajax({
//        url: '',
//        type: 'GET',
//        contentType: 'application/json',
//        data: JSON.stringify({
//            "seller_id": seller_id,
//            "product_id": product_id,
//        }),
//        success: function (response) {
//            console.log("Initial reviews fetched successfully");
//            console.log('Received Data:', response);
//            updateReviewsOnPage(response.data);
//        },
//        error: function (error) {
//            console.error("Error fetching initial reviews:", error);
//        },
//    });
//}



// Call fetchInitialReviews when the page loads
//$(document).ready(function () {
//    // Retrieve seller_id and product_id from the data attributes of the ul element
//    var seller_id = $('#reviews-list').data('seller-id');
//    var product_id = $('#reviews-list').data('product-id');
//
//    // Call fetchInitialReviews with retrieved seller_id and product_id
//    fetchInitialReviews(seller_id, product_id);
//});


 function updateStarRating(clickedRating) {
        const stars = document.querySelectorAll('.rating-wrapper img');

        // Remove 'rating-checked' class from all stars
        stars.forEach(star => star.classList.remove('rating-checked'));

        // Add 'rating-checked' class to clicked star and previous stars
        for (let i = 0; i < clickedRating; i++) {
            stars[i].classList.add('rating-checked');
        }

        // Update the hidden input field with the selected rating
        document.getElementById('rating').value = clickedRating;
    }

    function clearStarRating() {
        const stars = document.querySelectorAll('.rating-wrapper img');

        // Remove 'rating-checked' class from all stars
        stars.forEach(star => star.classList.remove('rating-checked'));

        // Clear the hidden input field
        document.getElementById('rating').value = '';
    }


    function customer_feedback(seller_id, product_id) {
        var rating = $('#rating').val();
        var review = $('#review').val();

        // Check if both fields are filled
        if (rating.trim() === '' || review.trim() === '') {
            alert("Please fill in both rating and review before submitting.");
            return;
        }


    // Testing codes
    console.log('Selected Rating:', rating);
    console.log('Review:', review);
    console.log('Seller Id:', seller_id)
    console.log('Product Id:', product_id)



        // You can proceed with your Ajax request here
        $.ajax({
            url: '',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                "request_type": "customer_feedback",
                "seller_id" : seller_id,
                "product_id" : product_id,
                "ratings": parseInt(rating),
                "reviews": review,
            }),
            success: function (response) {
                console.log("Feedback submitted successfully");
                alert("Your feedback has been submitted successfully");
                var updatedReviewsList = response.data;
                // Update the displayed reviews on the page
                updateReviewsOnPage(updatedReviewsList);
                console.log('Updated Reviews List:', updatedReviewsList);

            },
            error: function (error) {
                console.error("Error submitting feedback:", error);
                alert("An error occurred");
            },
        });
    }


// Function to update the displayed reviews on the page
function updateReviewsOnPage(reviewsList) {
    if (reviewsList && Array.isArray(reviewsList)) {
        var reviewsContainer = $('#reviews-list');
        reviewsContainer.empty();

        reviewsList.forEach(function (review) {
            var listItem = $('<li>').text('Rating: ' + review.rating + ', Review: ' + review.review);
            reviewsContainer.append(listItem);
        });
    } else {
        console.error('Invalid reviewsList:', reviewsList);
    }
}