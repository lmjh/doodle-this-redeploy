from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .webhook_handler import StripeWebhookHandler

import stripe


@require_POST
@csrf_exempt
def webhook(request):
    """
    Listens for webhooks from Stripe
    """
    # get secrets from settings
    wh_secret = settings.STRIPE_WEBHOOK_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # get webhook data and verify signature
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, wh_secret)
    except ValueError:
        # handle invalid payload error
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # handle invalid signature error
        return HttpResponse(status=400)
    except Exception as e:
        # handle other errors
        return HttpResponse(content=e, status=400)

    # create an instance of the StripeWebhookHandler class
    handler = StripeWebhookHandler(request)

    # create a dict to map event types against event handler functions
    handled_events = {
        "payment_intent.succeeded": handler.payment_intent_succeeded_handler,
        "payment_intent.payment_failed": handler.payment_intent_failed_handler,
    }

    # get the type of the received webhook event
    event_type = event["type"]

    # if the webhook event matches one of the keys in the handled_events dict
    if event_type in handled_events.keys():
        # set the event_handler to the matching function
        event_handler = handled_events[event_type]
    else:
        # otherwise, use the generic event handler
        event_handler = handler.generic_event_handler

    response = event_handler(event)
    return response
