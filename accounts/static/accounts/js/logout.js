document.getElementById('logout-button').addEventListener('click', function (ev) {
    ev.preventDefault();
    // if the user selected to clear their sketchbook 
    if ($('#clear-sketchbook-yes').prop('checked')) {
        // remove autosave
        localforage.removeItem('autosave')
            .then(
                // remove undocache
                localforage.removeItem('undoCache')
            )
            .then(
                // logout
                $('#logout').submit()
            );
    } else {
        // otherwise, just logout
        $('#logout').submit();
    }
});