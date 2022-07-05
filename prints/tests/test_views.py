import tempfile
from PIL import Image
from decimal import Decimal

from django.test import TestCase
from django.shortcuts import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.query import QuerySet
from django.contrib.auth.models import User

from prints.models import Product, ProductImage, ProductVariant
from accounts.models import Drawing


class TestShowAllPrintsView(TestCase):
    """
    Tests that the show_all_prints view is behaving as expected
    """

    def setUp(self):
        # create a ProductImage with a temporary file
        with tempfile.NamedTemporaryFile(suffix=".jpg") as temp_file:
            temp_image = Image.new("RGB", (10, 10))
            temp_image.save(temp_file, format="JPEG")
            temp_file.seek(0)

            # create ProductImage object
            product_image = ProductImage.objects.create(
                name_slug="test_image",
                image_type=".jpg",
                overlay_width="50%",
                overlay_x_offset="10%",
                overlay_y_offset="10%",
                image=SimpleUploadedFile(
                    name="temp_file.jpg",
                    content=temp_file.read(),
                ),
            )

        # create a Product
        product = Product.objects.create(
            image=product_image,
            name="test_product",
            display_name="Test Product",
            description="A product for testing",
            variant_type="CL",
        )

        # create a ProductVariant
        ProductVariant.objects.create(
            product=product,
            name="test_variant",
            display_name="Test Variant",
            price=Decimal("9.99"),
        )

    def tearDown(self):
        # delete all images from filesystem after running tests
        images = ProductImage.objects.all()
        for image in images:
            image.image.delete()

    def test_get_show_all_prints_page(self):
        response = self.client.get(reverse("show_all_prints"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "prints/show_all_prints.html")

    def test_view_returns_correct_contexts(self):
        response = self.client.get(reverse("show_all_prints"))

        self.assertIsInstance(response.context["products"], list)
        self.assertEqual(
            response.context["min_prices"], {"test_product": Decimal("9.99")}
        )


class TestProductDetailsView(TestCase):
    """
    Tests that the product_details view is behaving as expected
    """

    def setUp(self):
        # create a ProductImage with a temporary file
        with tempfile.NamedTemporaryFile(suffix=".jpg") as temp_file:
            temp_image = Image.new("RGB", (10, 10))
            temp_image.save(temp_file, format="JPEG")
            temp_file.seek(0)

            product_image = ProductImage.objects.create(
                name_slug="test_image",
                image_type=".jpg",
                overlay_width="50%",
                overlay_x_offset="10%",
                overlay_y_offset="10%",
                image=SimpleUploadedFile(
                    name="temp_file.jpg",
                    content=temp_file.read(),
                ),
            )

        # create a test user
        self.test_user = User.objects.create_user(
            username="testuser", password="123456"
        )

        # create a test drawing object with a temporary file
        with tempfile.NamedTemporaryFile(suffix=".jpg") as temp_file:
            temp_image = Image.new("RGB", (10, 10))
            temp_image.save(temp_file, format="JPEG")
            temp_file.seek(0)

            Drawing.objects.create(
                title="Saved Test Drawing",
                save_slot=1,
                user_account=self.test_user.useraccount,
                image=SimpleUploadedFile(
                    name="test_image.png",
                    content=temp_file.read(),
                ),
            )

        # create a Product
        product = Product.objects.create(
            image=product_image,
            name="test_product",
            display_name="Test Product",
            description="A product for testing",
            variant_type="CL",
        )

        # create a ProductVariant
        ProductVariant.objects.create(
            product=product,
            name="test_variant",
            display_name="Test Variant",
            description="A variant for testing",
            price=Decimal("9.99"),
        )

    def tearDown(self):
        # delete all images from filesystem after running tests
        images = ProductImage.objects.all()
        for image in images:
            image.image.delete()
        drawings = Drawing.objects.all()
        for drawing in drawings:
            drawing.image.delete()

    def test_get_product_details_page(self):
        product = Product.objects.get(pk=1)
        response = self.client.get(
            reverse("product_details", args=(product.name,))
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "prints/product_details.html")

    def test_view_returns_correct_contexts(self):
        self.client.login(username="testuser", password="123456")
        product = Product.objects.get(pk=1)
        response = self.client.get(
            reverse("product_details", args=(product.name,))
        )

        self.assertEqual(response.context["product"], product)
        self.assertIsInstance(response.context["variants"], QuerySet)
        self.assertIsInstance(response.context["saved_drawings"], QuerySet)
        self.assertIsInstance(
            response.context["json_data"]["drawingUrls"][1], str
        )
        self.assertEqual(
            response.context["json_data"]["variantPrices"][1], Decimal("9.99")
        )
        self.assertIsInstance(
            response.context["json_data"]["variantUrls"]["default"], str
        )
        self.assertEqual(
            response.context["json_data"]["overlay"]["default"],
            ["50%", "10%", "10%"],
        )
        self.assertEqual(
            response.context["json_data"]["placeholder"],
            "/media/svg/placeholder.svg",
        )
