import tempfile
from PIL import Image
from decimal import Decimal

from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from prints.models import ProductVariant, ProductImage, Product
from accounts.models import Drawing


class TestCartContentsContext(TestCase):
    """
    Tests that the cart_contents context processor is behaving as expected.
    """

    def setUp(self):
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

        # create two ProductVariants
        ProductVariant.objects.create(
            image=product_image,
            product=product,
            display_name="Test Variant",
            name="test_variant",
            price=Decimal(1.99),
            sku="TEST-1",
        )

        ProductVariant.objects.create(
            product=product,
            display_name="Test Variant 2",
            name="test_variant_2",
            price=Decimal(2.99),
            sku="TEST-2",
        )

    def tearDown(self):
        # delete all images from filesystem after running tests
        images = ProductImage.objects.all()
        for image in images:
            image.image.delete()

    def test_correct_context_variables_returned(self):
        response = self.client.get(reverse("view_cart"))
        self.assertIn("cart_contents", response.context)
        self.assertIn("items_total", response.context)
        self.assertIn("cart_count", response.context)
        self.assertIn("delivery", response.context)
        self.assertIn("grand_total", response.context)

    def test_correct_cart_contents_returned(self):
        session = self.client.session
        session["cart"] = [{"variant_id": "1", "drawing": "0", "quantity": 2}]
        session.save()
        response = self.client.get(reverse("view_cart"))
        self.assertEqual("0", response.context["cart_contents"][0]["drawing"])
        self.assertEqual(
            "/media/svg/blank.svg",
            response.context["cart_contents"][0]["drawing_image"],
        )
        self.assertIn("image", response.context["cart_contents"][0])
        self.assertEqual(
            "Test Product - Test Variant",
            response.context["cart_contents"][0]["name"],
        )
        self.assertEqual("3.98", response.context["cart_contents"][0]["price"])
        self.assertEqual(
            "1.99", response.context["cart_contents"][0]["price_each"]
        )
        self.assertEqual(2, response.context["cart_contents"][0]["quantity"])
        self.assertEqual(
            "1", response.context["cart_contents"][0]["variant_id"]
        )

    def test_correct_cart_count_returned(self):
        session = self.client.session
        session["cart"] = [
            {"variant_id": "1", "drawing": "0", "quantity": 1},
            {"variant_id": "1", "drawing": "1", "quantity": 2},
            {"variant_id": "2", "drawing": "0", "quantity": 3},
            {"variant_id": "2", "drawing": "1", "quantity": 4},
        ]
        session.save()
        self.client.login(username="testuser", password="123456")
        response = self.client.get(reverse("view_cart"))
        self.assertEqual(10, response.context["cart_count"])

    def test_cart_count_cannot_exceed_99(self):
        session = self.client.session
        session["cart"] = [
            {"variant_id": "1", "drawing": "0", "quantity": 100},
        ]
        session.save()
        response = self.client.get(reverse("view_cart"))
        self.assertEqual("99+", response.context["cart_count"])

    def test_correct_item_total_returned(self):
        session = self.client.session
        session["cart"] = [
            {"variant_id": "1", "drawing": "0", "quantity": 1},
            {"variant_id": "1", "drawing": "1", "quantity": 2},
            {"variant_id": "2", "drawing": "0", "quantity": 3},
            {"variant_id": "2", "drawing": "1", "quantity": 4},
        ]
        session.save()
        self.client.login(username="testuser", password="123456")
        response = self.client.get(reverse("view_cart"))
        self.assertEqual("26.90", response.context["items_total"])

    def test_correct_grand_total_returned(self):
        session = self.client.session
        session["cart"] = [
            {"variant_id": "1", "drawing": "0", "quantity": 1},
            {"variant_id": "1", "drawing": "1", "quantity": 2},
            {"variant_id": "2", "drawing": "0", "quantity": 3},
            {"variant_id": "2", "drawing": "1", "quantity": 4},
        ]
        session.save()
        self.client.login(username="testuser", password="123456")
        response = self.client.get(reverse("view_cart"))
        self.assertEqual("29.90", response.context["grand_total"])
