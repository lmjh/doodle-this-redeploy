// declare toastCount at top level to allow generating a unique id for each toast
let toastCount = 0;

$( document ).ready(function() {
    // find and parse the json_messages element rendered by the template
    let messages = JSON.parse(document.getElementById('json_messages').textContent);
    // if the array contains messages
    if (messages) {
        // call the displayToast function for each message
        messages.forEach(function (message) {
            displayToast(message.tag, message.message);
        });
    }
});

/**
 * Returns an html toast template populated with the received tag, message and toastCount data.
 */
function generateToast(tag, message, toastCount) {
    // create variables 
    let role = "";
    let aria = "";
    let cssClass = "";
    let timeout = "";

    // assign role, aria-live region type, class and timeout based on tag
    switch (tag) {
        case "debug":
            role = "alert";
            aria = "assertive";
            cssClass = "toast-debug";
            timeout = "data-bs-autohide='false'"; // do not timeout debug messages
            break;
        case "info":
            role = "status";
            aria = "polite";
            cssClass = "toast-info";
            timeout = "data-bs-delay='10000'"; // 10 second delay
            break;
        case "success":
            role = "status";
            aria = "polite";
            cssClass = "toast-success";
            timeout = "data-bs-delay='10000'";
            break;
        case "warning":
            role = "alert";
            aria = "assertive";
            cssClass = "toast-warning";
            timeout = "data-bs-delay='10000'";
            break;
        case "error":
            role = "alert";
            aria = "assertive";
            cssClass = "toast-error";
            timeout = "data-bs-delay='10000'";
            break;
        default:
            role = "status";
            aria = "polite";
            cssClass = "toast-info";
            timeout = "data-bs-delay='10000'";
    }

    // generate and return toast template
    let toastTemplate = 
    `<div role="${role}" aria-live="${aria}" aria-atomic="true" class="toast align-items-center border-0 ${cssClass}" 
        id="toast-${toastCount}" ${timeout}>
        <div class='toast-header'></div>
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    </div>`;
    return toastTemplate;
}

/**
 * Creates and displays a toast notification using the given tag and message.
 * Adds an event listener to remove the toast from the DOM after it has been hidden.
 * Increments the toastCount variable to give toasts a unique id.
 */
function displayToast(tag, message) {
    // call the generateToast function to create a new toast
    let newToastTemplate = generateToast(tag, message, toastCount);

    // add the toast to the #toast-container element
    $('#toast-container').append(newToastTemplate);

    // find the new toast using its id
    let newToastElement = document.getElementById(`toast-${toastCount}`);

    // create a bootstrap Toast object with the toast and show it
    let newToast = new bootstrap.Toast(newToastElement);
    newToast.show();

    // add an event listener to destroy the toast after its display timer runs out
    newToastElement.addEventListener('hidden.bs.toast', function(event) {
        event.target.remove();
    });

    // increment the toast counter
    toastCount += 1;
}