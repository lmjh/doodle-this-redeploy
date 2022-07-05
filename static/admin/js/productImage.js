/* jshint esversion: 11, jquery: true */
// add event listener to wait for DOM to load
document.addEventListener("DOMContentLoaded", function () {
    // find overlay and input elements
    const overlay = document.getElementById('overlay');
    const overlayWidth = document.getElementById('id_overlay_width');
    const overlayX = document.getElementById('id_overlay_x_offset');
    const overlayY = document.getElementById('id_overlay_y_offset');
    const imageUpload = document.getElementById('id_image');

    // set overlay width, x offset and y offset
    overlay.style.width = overlayWidth.value;
    overlay.style.left = overlayX.value;
    overlay.style.top = overlayY.value;

    // add event listeners to update overlay width and offsets as user changes the input fields
    overlayWidth.addEventListener('input', function () {
        overlay.style.width = overlayWidth.value;
    });
    overlayX.addEventListener('input', function () {
        overlay.style.left = overlayX.value;
    });
    overlayY.addEventListener('input', function () {
        overlay.style.top = overlayY.value;
    });

    // add event listener to change preview image when a new file is selected
    imageUpload.addEventListener('change', function () {
        let preview = document.getElementById('preview');
        // if preview is found, replace with new image
        if (preview) {
            preview.onload = function () {
                // revoke object URL after image is loaded
                URL.revokeObjectURL(preview.src);
            };
            // create object URL from selected file and assign as src of preview image
            preview.src = URL.createObjectURL(imageUpload.files[0]);
        } else {
            // if preview is not found, create preview image and set id to 'preview'
            preview = document.createElement('img');
            preview.id = "preview";
            preview.alt= "Product image preview";
            preview.onload = function () {
                // revoke object URL after image is loaded
                URL.revokeObjectURL(preview.src);
                // append preview image to image holder 
                document.getElementById("image-holder").appendChild(preview);
                // make overlay visible
                overlay.style.visibility = "visible";
            };
            // create object URL from selected file and assign as src of preview image
            preview.src = URL.createObjectURL(imageUpload.files[0]);
        }
    });
});