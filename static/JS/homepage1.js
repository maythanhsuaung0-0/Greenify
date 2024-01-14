document.addEventListener('DOMContentLoaded', () => {
    const nxtButtons = document.querySelectorAll('.nxt-btn');
    const preButtons = document.querySelectorAll('.pre-btn');

    nxtButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Find the closest parent section and then find the product-container within it
            let container = button.closest('.product').querySelector('.product-container');
            console.log('Next button clicked');
            container.scrollLeft += 200; // Scroll by 200px, adjust as needed
        });
    });

    preButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Find the closest parent section and then find the product-container within it
            let container = button.closest('.product').querySelector('.product-container');
            console.log('Previous button clicked');
            container.scrollLeft -= 200; // Scroll by 200px, adjust as needed
        });
    });
});
