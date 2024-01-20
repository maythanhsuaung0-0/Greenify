document.addEventListener("DOMContentLoaded", () => {
        const image = document.getElementById("previewImage");
        const input = document.getElementById("fileInput");

        input.addEventListener("change", () => {
            if (input.files.length > 0) {
                // Set the src attribute of the image to the URL of the selected file
                image.src = URL.createObjectURL(input.files[0]);
            } else {
                // Optionally handle the case where no file is selected
                console.warn("No file selected.");
                // Set a placeholder image path when no file is selected
                image.src = "/static/images/placeholder.jpg";
            }
        });
        });