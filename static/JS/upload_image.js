document.addEventListener('DOMContentLoaded', function() {
    var fileInput = document.getElementById('fileInput');
    var previewImage = document.getElementById('previewImage');

    if (fileInput && previewImage) {
        fileInput.addEventListener('change', function(event) {
            console.log('Before preventDefault');
            event.preventDefault();
            console.log('After preventDefault');

            var file = fileInput.files[0];
            var reader = new FileReader();

            reader.onload = function(e) {
                previewImage.src = e.target.result;
            };

            reader.readAsDataURL(file);
        });
    }
});
