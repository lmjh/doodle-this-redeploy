from django.conf import settings
from django.shortcuts import get_object_or_404

from prints.models import ProductVariant
from accounts.models import Drawing


def cart_contents(request):
    """
    Handles user shopping cart contents data
    """

    # get cart contents
    cart_contents = request.session.get("cart", [])
    cart_count = 0

    # create list to store cart items that are found
    cleaned_cart = []

    # instantiate variable for total costs
    items_total = 0

    # iterate over items in cart
    for item in cart_contents:
        # find product variant. Resolves to None if variant not found
        variant = ProductVariant.objects.filter(pk=item["variant_id"]).first()
        if variant:
            # if the variant is found, add it to the cleaned_cart list
            cleaned_cart.append(item)
            # set drawing_image to the url of the saved drawing or a default
            # blank image if the current sketchbook drawing was selected
            if item["drawing"] == "0":
                item["drawing_image"] = settings.MEDIA_URL + "svg/blank.svg"
            else:
                drawing = Drawing.objects.filter(
                    user_account=request.user.pk,
                    save_slot=item["drawing"],
                ).first()
                if drawing:
                    item["drawing_image"] = drawing.image.url
            # add variant price * quantity to items_total
            items_total += variant.price * item["quantity"]
            # generate the product variant's name
            item[
                "name"
            ] = f"{variant.product.display_name} - {variant.display_name}"
            # add the image url of the variant, if available
            if variant.image:
                item["image"] = variant.image.image.url
            # use product image if no variant image available
            else:
                item["image"] = variant.product.image.image.url

            item["price_each"] = f'{variant.price}'
            item_price = variant.price * item["quantity"]
            item["price"] = f'{item_price}'

            cart_count += item["quantity"]

    # update the session cart with the cleaned cart list to remove any product
    # variants in the cart that weren't found in the database 
    request.session["cart"] = cleaned_cart

    delivery = settings.STANDARD_DELIVERY_FEE

    grand_total = items_total + delivery

    # pass variables to context
    context = {
        "cart_contents": cart_contents,
        "items_total": f'{items_total}',
        "cart_count": cart_count if cart_count < 100 else "99+",
        "delivery": f'{delivery}',
        "grand_total": f'{grand_total}',
    }

    return context
