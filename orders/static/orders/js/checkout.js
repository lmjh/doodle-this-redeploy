// INITIALISE ELEMENTS AND STYLES

// retrieve Stripe public key and client secret from page
const stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
const clientSecret = $('#id_client_secret').text().slice(1, -1);

// get the csrf token from the form
const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

// initialise stripe with key and instantiate stripe elements
const stripe = Stripe(stripePublicKey);
const elements = stripe.elements();

// retrieve variable representing if user has current drawing in cart
const currentDrawingInCart = JSON.parse(document.getElementById('current_drawing_in_cart').textContent);

// create style variable to add styles to card
const style = {
    base: {
        iconColor: '#ebebeb',
        color: '#ebebeb',
        backgroundColor: '#202020',
        fontFamily: '"Quicksand", Arial, Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#ebebeb'
        }
    },
    invalid: {
        color: '#ff3a3a',
        iconColor: '#ff3a3a'
    }
};

// instantiate card with style variable and mount to checkout page element
const card = elements.create('card', {
    style: style
});
card.mount('#card-element');

// assign payment form to a const
const form = document.getElementById('payment-form');

// DECLARE FUNCTIONS

/**
 * disables the card and form elements and shows the loading overlay 
 */
function deactivateElements() {
    card.update({
        'disabled': true
    });
    $('#submit-order').attr('disabled', true);
    // hide the payment form and show the loading overlay
    $('#payment-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);
}

/**
 * re-enables the card and form elements and hides the loading overlay 
 */
function activateElements() {
    // re-enable card and submit elements to allow user to fix error
    card.update({
        'disabled': false
    });
    $('#submit-order').attr('disabled', false);
    // show the payment form and hide loading overlay
    $('#payment-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);
}

/**
 * Populates the stripe confirmCardPayment function with payment and shipping details. Returns errors if
 * payment is not successful and submits form if payment is successful.
 */
function confirmStripePayment() {
    // set saveDetails to true if user clicked save details checkbox, false otherwise
    let saveDetails = Boolean($('#save-details').attr('checked'));

    // bundle data to be submitted in an object
    let postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
        'save_details': saveDetails,
    };
    let cacheUrl = '/orders/cache_order_data/';

    // post the data to the cache_checkout_data view.
    // if response code is 200, then execute stripe confirm card payment functions
    $.post(cacheUrl, postData).done(function () {
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                // fill billing details with form data
                billing_details: {
                    // concatenate first and last names
                    name: $.trim(form.first_name.value) + " " + $.trim(form.last_name.value),
                    phone: $.trim(form.phone_number.value),
                    email: $.trim(form.email_address.value),
                    address: {
                        line1: $.trim(form.address_1.value),
                        line2: $.trim(form.address_2.value),
                        city: $.trim(form.town.value),
                        state: $.trim(form.county.value),
                        country: $.trim(form.country.value),
                    }
                }
            },
            shipping: {
                // concatenate first and last names
                name: $.trim(form.first_name.value) + " " + $.trim(form.last_name.value),
                phone: $.trim(form.phone_number.value),
                address: {
                    line1: $.trim(form.address_1.value),
                    line2: $.trim(form.address_2.value),
                    city: $.trim(form.town.value),
                    state: $.trim(form.county.value),
                    country: $.trim(form.country.value),
                    postal_code: $.trim(form.postcode.value),
                }
            },
        }).then(function (result) {
            // if error returned, display it
            if (result.error) {
                let errorDiv = document.getElementById('card-errors');
                let errorHtml = `
            <div class='card-errors'>
                <span class="icon" role="alert">
                <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>
            </div>
            `;
                $(errorDiv).html(errorHtml);
                activateElements();
            } else {
                // if payment succeeds, submit the form
                if (result.paymentIntent.status === 'succeeded') {
                    form.submit();
                }
            }
        });
    }).fail(function () {
        // reload page if post function fails
        location.reload();
    });
}

// ADD EVENT LISTENERS

// add event listener to check for card errors and display them
card.addEventListener('change', function (event) {
    let errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
        <div class='card-errors'>
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        </div>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

// add an event listener to the payment form to submit payments
form.addEventListener('submit', function (ev) {
    // prevent submit button default actions and disable form and button
    ev.preventDefault();
    deactivateElements();

    // check if user has requested a print of their current sketchbook's drawing
    if (currentDrawingInCart) {
        // if so, retrieve the drawing from the autosave in local storage
        localforage.getItem('autosave').then(function (blob) {
            // create a FormData object and append the csrf token, stripe intent id and image 
            let cacheForm = new FormData();
            cacheForm.append('csrfmiddlewaretoken', csrfToken);
            cacheForm.append('stripe_pid', clientSecret.split('_secret')[0]);
            cacheForm.append('image', blob, 'drw.png');
            // submit to the cache_order_drawing view
            let cacheDrawingUrl = '/orders/cache_order_drawing/';
            $.ajax({
                    type: 'POST',
                    url: cacheDrawingUrl,
                    enctype: 'multipart/form-data',
                    data: cacheForm,
                    cache: false,
                    // set contentType and processData to false to allow passing files
                    // to the server
                    contentType: false,
                    processData: false,
                })
                // call the confirmStripePayment function when done
                .done(confirmStripePayment)
                .fail(function (error) {
                    // display an error if ajax post fails
                    displayToast('error', 'Something seems to have gone wrong. Please try again.');
                    activateElements();
                });
        }).catch(function (err) {
            // if the drawing is not found, show an error message
            displayToast('error', 'No current sketchbook doodle found. Please try again or print from an account save slot.');
            activateElements();
        });
    } else {
        // if the user hasn't requested a print of their current sketchbook's drawing, just call confirmStripePayment function
        confirmStripePayment();
    }
});