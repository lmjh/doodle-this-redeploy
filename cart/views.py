from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.contrib.humanize.templatetags.humanize import apnumber

from prints.models import ProductVariant


def view_cart(request):
    """
    A view to display the contents of the user's shopping cart
    """

    template = "cart/cart.html"
    return render(request, template)


def add_to_cart(request):
    """
    A view to add items to the user's shopping cart
    """
    if request.method == "POST":
        # gather data from POST request
        variant_id = request.POST.get("variant")
        get_object_or_404(ProductVariant, pk=variant_id)
        quantity = int(request.POST.get("quantity"))
        drawing = request.POST.get("drawing")
        redirect_url = request.POST.get("redirect_url")

        # get cart from session or set to an empty list if not found
        cart = request.session.get("cart", [])

        # declare a variable to record if the variant/drawing pair is already
        # in the cart
        in_cart = False
        # iterate throught the cart list
        for item in cart:
            # if the list contains an object with the same variant id and
            # drawing as the request
            if item["variant_id"] == variant_id and item["drawing"] == drawing:
                # increase that object's quantity and set in_cart to true
                item["quantity"] += quantity
                in_cart = True
                # get view cart url
                checkout_url = reverse("view_cart")
                # Convert number to word if < 10 and pluralise if > 1
                quantity_string = (
                    apnumber(quantity).capitalize()
                    + " product"
                    + ("s" if quantity > 1 else "")
                )

                # send success message
                messages.success(
                    request,
                    f"{quantity_string} added to shopping cart. "
                    f"<div class='text-center'><a href='{checkout_url}' class="
                    f"'btn btn-brand-primary bg-primary mt-3 w-75'>Checkout "
                    f"Now</a></div>",
                )

        # if no matching object was found
        if in_cart is False:
            # add an object to the cart using the submitted data
            item = {
                "variant_id": variant_id,
                "drawing": drawing,
                "quantity": quantity,
            }
            cart.append(item)
            # get view cart url
            checkout_url = reverse("view_cart")
            # Convert number to word if < 10 and pluralise if > 1
            quantity_string = (
                apnumber(quantity).capitalize()
                + " product"
                + ("s" if quantity > 1 else "")
            )

            # send success message
            messages.success(
                request,
                f"{quantity_string} added to shopping cart. <div class='"
                f"text-center'><a href='{checkout_url}' class= 'btn btn-brand-"
                f"primary bg-primary mt-3 w-75'>Checkout Now</a></div>",
            )

        request.session["cart"] = cart

        return redirect(redirect_url)


def update_cart_item(request):
    """
    A view to update the quantity of an item in the shopping cart
    """
    if request.method == "POST":
        # gather data from request
        variant_id = request.POST.get("variant_id")
        drawing = request.POST.get("drawing")
        quantity = int(request.POST.get("quantity"))

        # get cart from session
        cart = request.session.get("cart", [])

        # iterate over a copy of the cart, enumerate to access loop index
        # (https://stackoverflow.com/a/10665631)
        for index, item in enumerate(cart[:]):
            # find the item matching the variant_id and selected drawing
            if item["variant_id"] == variant_id and item["drawing"] == drawing:
                # remove from the cart list if quantity is zero
                if quantity == 0:
                    cart.remove(item)
                    messages.success(
                        request,
                        "Item removed from shopping cart.",
                    )
                # update the cart item's quantity if greater than zero
                else:
                    cart[index]["quantity"] = quantity
                    messages.success(
                        request,
                        "Shopping cart quantity updated.",
                    )

        # update session cart and redirect to view_cart page
        request.session["cart"] = cart
        return redirect(reverse("view_cart"))


def remove_cart_item(request):
    """
    A view to remove an item from the shopping cart
    """
    if request.method == "POST":
        # gather data from request
        variant_id = request.POST.get("variant_id")
        drawing = request.POST.get("drawing")

        # get cart from session
        cart = request.session.get("cart", [])

        # iterate over a copy of the cart
        for item in cart[:]:
            # find the item matching the variant_id and selected drawing
            if item["variant_id"] == variant_id and item["drawing"] == drawing:
                # remove from the cart list
                cart.remove(item)
                messages.success(
                    request,
                    "Item removed from shopping cart.",
                )

        # update session cart and redirect to view_cart page
        request.session["cart"] = cart
        return redirect(reverse("view_cart"))
