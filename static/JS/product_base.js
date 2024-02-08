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

// Ratings and Reviews
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

// Function to clear the rating and review inputs
function clearRatingAndReviewInputs() {
    // Clear the rating input
    $('#rating').val('');

    // Clear the review textarea
    $('#review').val('');

    // Clear the star rating display
    clearStarRating();
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
            clearRatingAndReviewInputs();

        },
        error: function (error) {
            console.error("Error submitting feedback:", error);
            alert("An error occurred");
        },
    });
}

// Function to fetch reviews for the see reviews button
function fetchReviews(seller_id, product_id) {
    $.ajax({
        url: '',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            "request_type": "fetch_reviews",
            "seller_id" : seller_id,
            "product_id" : product_id
        }),
        success: function(response) {
            console.log("Reviews fetched successfully");
            var reviewsList = response.data;
            updateReviewsOnPage(reviewsList);
        },
        error: function(error) {
            console.error("Error fetching reviews:", error);
            alert("An error occurred while fetching reviews");
        }
    });
}

// Function to update the displayed reviews on the page
function updateReviewsOnPage(reviewsList) {
    var reviewsContainer = $('#reviews-list');

    if (Array.isArray(reviewsList) && reviewsList.length >  0) {
        reviewsContainer.empty();
        reviewsList.forEach(function (review) {
            var reviewDate = new Date(review.timestamp);

            // Format date
            var formattedDate = reviewDate.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });

            var reviewHTML =
                 '<p><strong>Date:</strong> ' + formattedDate + '</p>' +
                 '<p><strong>Rating:</strong> ' + review.rating + '</p>' +
                 '<p><strong>Review:</strong> ' + review.review + '</p>' +
                 '<hr style="border-top: 3px solid #bbb">';

            reviewsContainer.append(reviewHTML);
        });
    } else {
        reviewsContainer.empty();
        var noReviewsMessage = $('<p>').text('No reviews');
        reviewsContainer.append(noReviewsMessage);
        console.error('Invalid reviewsList:', reviewsList);
    }
}