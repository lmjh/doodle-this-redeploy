$(document).ready(function () {
    // retrieve the autosave of the current drawing from localforage 
    localforage.getItem('autosave').then(function (blob) {
        // create an objectURL for the saved drawing 
        let autosaveURL = blob ? URL.createObjectURL(blob) : false;
        // iterate through images on page
        $('.drawing-thumbnail').each(function () {
            // if the image's src is the default blank image
            if ($(this).attr('src').slice(-9) == 'blank.svg' && autosaveURL) {
                // replace it with the autosave image
                $(this).attr('src', autosaveURL);
            }
        });
        // revoke object url after a short delay to allow time for image to load
        setTimeout(function () {
            URL.revokeObjectURL(autosaveURL);
        }, 200);
    });
});