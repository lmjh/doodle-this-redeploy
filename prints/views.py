from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import RestrictedError

from .models import Product, ProductVariant, ProductImage
from accounts.models import Drawing
from prints.forms import ProductForm, ProductImageForm, ProductVariantForm


def show_all_prints(request):
    """
    A view to display all available print product in the shop
    """

    # get all products
    all_products = Product.objects.all()

    # create a dict to hold minimum prices
    min_prices = {}

    # create list to hold products with variants
    products_with_variants = []

    # iterate through products
    for product in all_products:
        # find variants for each product and order by price
        variants = ProductVariant.objects.filter(product=product.pk).order_by(
            "price"
        )
        if variants:
            # if a variant is found, add the product to the
            # products_with_variants list
            products_with_variants.append(product)
            # add min_price for each product to the min_prices dict
            min_prices[product.name] = variants[0].price

    template = "prints/show_all_prints.html"
    context = {
        "products": products_with_variants,
        "min_prices": min_prices,
    }

    return render(request, template, context)


def product_details(request, product_name):
    """
    A view to display details of a product and allow a user to select options
    to purchase
    """

    product = get_object_or_404(Product, name=product_name)
    variants = ProductVariant.objects.filter(product=product.pk)
    saved_drawings = Drawing.objects.filter(user_account=request.user.pk)

    # create dict to store data to be passed to page javascript
    json_data = {}
    # use dict comprehension to store urls of user's saved drawings, variant
    # prices, product image urls, and descriptions
    json_data["drawingUrls"] = {
        drawing.save_slot: drawing.image.url for drawing in saved_drawings
    }
    json_data["variantPrices"] = {
        variant.id: variant.price for variant in variants
    }
    json_data["variantDescriptions"] = {
        variant.id: variant.description for variant in variants
    }
    # if a variant has an image attached, store its url
    json_data["variantUrls"] = {
        variant.id: variant.image.image.url
        for variant in variants
        if variant.image
    }
    # add the image url for the default product image
    json_data["variantUrls"]["default"] = product.image.image.url
    # if a variant has an image attached, add the overlay data for that image
    # to an array
    json_data["overlay"] = {
        variant.id: [
            variant.image.overlay_width,
            variant.image.overlay_x_offset,
            variant.image.overlay_y_offset,
        ]
        for variant in variants
        if variant.image
    }
    # add the overlay data for the default product image
    json_data["overlay"]["default"] = [
        product.image.overlay_width,
        product.image.overlay_x_offset,
        product.image.overlay_y_offset,
    ]
    # add the url for the paceholder image
    json_data["placeholder"] = settings.MEDIA_URL + "svg/placeholder.svg"

    template = "prints/product_details.html"
    context = {
        "product": product,
        "variants": variants,
        "saved_drawings": saved_drawings,
        "json_data": json_data,
    }

    return render(request, template, context)


@staff_member_required
def product_management(request):
    """
    A view to house links to other product management tools
    @staff_member_required decorator restricts this view to staff members
    """

    products = Product.objects.all()
    product_variants = ProductVariant.objects.all()
    product_images = ProductImage.objects.all()

    template = "prints/product_management.html"

    context = {
        "products": products,
        "product_variants": product_variants,
        "product_images": product_images,
    }

    return render(request, template, context)


@staff_member_required
def add_product(request):
    """
    A view to add products to the database.
    @staff_member_required decorator restricts this view to staff members
    """

    # if request is POST
    if request.method == "POST":
        # fill form from POST data
        form = ProductForm(request.POST)
        # if form is valid
        if form.is_valid():
            # save and redirect
            form.save()
            messages.success(
                request,
                "Product added to database. Note: The product will not appear "
                "on the Prints page until a variant is added to it.",
            )
            return redirect(reverse("product_management"))
        else:
            messages.error(request, "Form invalid. Please check and try again")
    else:
        form = ProductForm()

    template = "prints/add_product.html"
    context = {"form": form}
    return render(request, template, context)


@staff_member_required
def edit_product(request, product_id):
    """
    A view to edit products.
    @staff_member_required decorator restricts this view to staff members
    """

    # get product or 404 if not found
    product = get_object_or_404(Product, pk=product_id)

    # if request is POST
    if request.method == "POST":
        # set form instance to product and fill from POST data
        form = ProductForm(request.POST, instance=product)
        # if form is valid
        if form.is_valid():
            # save and redirect
            form.save()
            messages.success(
                request, "The product has been successfully updated."
            )
            return redirect(reverse("product_management"))
        else:
            messages.error(request, "Form invalid. Please check and try again")
    else:
        form = ProductForm(instance=product)

    template = "prints/edit_product.html"
    context = {"form": form, "product": product}
    return render(request, template, context)


@staff_member_required
def delete_product(request, product_id):
    """
    A view to delete products.
    @staff_member_required decorator restricts this view to staff members
    """

    # get product or 404 if not found
    product = get_object_or_404(Product, pk=product_id)
    # try to delete product
    try:
        product.delete()
    except RestrictedError as error:
        # a RestrictedError will be returned if the product has one or more
        # ProductVariants pointing to it
        error_string = ""
        # iterate through restricted objects in error and add to list
        for restricted_object in error.restricted_objects:
            sku = restricted_object.sku
            error_string += f"<li>Variant SKU: {sku}</li>"

        # return list of objects preventing deletion of image
        messages.error(
            request,
            f"Unable to delete this product as it is in use by the following "
            f"variant(s):<ul>{error_string}</ul>",
        )
        return redirect(reverse("product_management"))

    # add success message and redirect to product management page
    messages.success(request, "The product has been deleted.")
    return redirect(reverse("product_management"))


@staff_member_required
def add_product_image(request):
    """
    A view to add product images to the database.
    @staff_member_required decorator restricts this view to staff members
    """

    # if request is POST
    if request.method == "POST":
        # fill form from POST data
        form = ProductImageForm(request.POST, request.FILES)

        # if form is valid
        if form.is_valid():
            # save and redirect
            form.save()
            messages.success(
                request, "Product Image successfully added to database."
            )
            return redirect(reverse("product_management"))
        else:
            messages.error(request, "Form invalid. Please check and try again")
    else:
        form = ProductImageForm()

    template = "prints/add_product_image.html"
    context = {"form": form}
    return render(request, template, context)


@staff_member_required
def edit_product_image(request, product_image_id):
    """
    A view to edit product images in the database.
    @staff_member_required decorator restricts this view to staff members
    """
    product_image = get_object_or_404(ProductImage, pk=product_image_id)

    # if request is POST
    if request.method == "POST":
        # fill form from POST data
        form = ProductImageForm(
            request.POST, request.FILES, instance=product_image
        )

        # if form is valid
        if form.is_valid():
            # save and redirect
            form.save()
            messages.success(request, "Product Image successfully updated.")
            return redirect(reverse("product_management"))
        else:
            messages.error(request, "Form invalid. Please check and try again")
    else:
        form = ProductImageForm(instance=product_image)

    template = "prints/edit_product_image.html"
    context = {"form": form, "product_image": product_image}
    return render(request, template, context)


@staff_member_required
def delete_product_image(request, product_image_id):
    """
    A view to delete product images.
    @staff_member_required decorator restricts this view to staff members
    """

    # get product image or 404 if not found
    product_image = get_object_or_404(ProductImage, pk=product_image_id)
    # try to delete product image
    try:
        product_image.delete()
    except RestrictedError as error:
        # a RestrictedError will be returned if the image is in use by one or
        # more Products or ProductVariants
        error_string = ""
        # iterate through restricted objects in error and add to list
        for restricted_object in error.restricted_objects:
            if isinstance(restricted_object, Product):
                product = restricted_object.display_name
                error_string += (
                    f"<li>Product: {product}</li>"
                )
            else:
                sku = restricted_object.sku
                error_string += f"<li>Variant SKU: {sku}</li>"

        # return list of objects preventing deletion of image
        messages.error(
            request,
            f"Unable to delete this image as it is in use by the following "
            f"object(s):<ul>{error_string}</ul>",
        )
        return redirect(reverse("product_management"))

    # add success message and redirect to product management page
    messages.success(request, "The product image has been deleted.")
    return redirect(reverse("product_management"))


@staff_member_required
def add_product_variant(request):
    """
    A view to add product variants to the database.
    @staff_member_required decorator restricts this view to staff members
    """

    # if request is POST
    if request.method == "POST":
        # fill form from POST data
        form = ProductVariantForm(request.POST)
        # if form is valid
        if form.is_valid():
            # save and redirect
            form.save()
            messages.success(
                request, "Product variant successfully added to database."
            )
            return redirect(reverse("product_management"))
        else:
            messages.error(request, "Form invalid. Please check and try again")
    else:
        form = ProductVariantForm()

    template = "prints/add_product_variant.html"
    context = {"form": form}
    return render(request, template, context)


@staff_member_required
def edit_product_variant(request, product_variant_id):
    """
    A view to edit product variants in the database.
    @staff_member_required decorator restricts this view to staff members
    """

    product_variant = get_object_or_404(ProductVariant, pk=product_variant_id)
    # if request is POST
    if request.method == "POST":
        # set form instance to product variant and fill from POST data
        form = ProductVariantForm(request.POST, instance=product_variant)
        # if form is valid
        if form.is_valid():
            # save and redirect
            form.save()
            messages.success(request, "Product variant successfully updated.")
            return redirect(reverse("product_management"))
        else:
            messages.error(request, "Form invalid. Please check and try again")
    else:
        form = ProductVariantForm(instance=product_variant)

    template = "prints/edit_product_variant.html"
    context = {"form": form, "product_variant": product_variant}
    return render(request, template, context)


@staff_member_required
def delete_product_variant(request, product_variant_id):
    """
    A view to delete product variants from the database.
    @staff_member_required decorator restricts this view to staff members
    """

    # find variant or return 404
    product_variant = get_object_or_404(ProductVariant, pk=product_variant_id)

    # delete variant
    product_variant.delete()

    # add success message and redirect to product management page
    messages.success(request, "The product variant has been deleted.")
    return redirect(reverse("product_management"))
