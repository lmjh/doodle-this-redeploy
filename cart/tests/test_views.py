import tempfile
from PIL import Image
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from prints.models import ProductVariant, Product, ProductImage


class TestViewCartView(TestCase):
    """
    Tests that the view_cart view is behaving as expected.
    """

    def test_get_view_cart_page(self):
        response = self.client.get(reverse("view_cart"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cart/cart.html")


class TestAddToCartView(TestCase):
    """
    Tests that the add_to_cart view is behaving as expected.
    """

    def setUp(self):
        # create a test user
        self.test_user = User.objects.create_user(
            username="testuser", password="123456"
        )

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
            display_name="Test Variant",
            name="test_variant",
            price=Decimal(1.99),
            sku="TEST-1",
        )

    def tearDown(self):
        # delete all images from filesystem after running tests
        images = ProductImage.objects.all()
        for image in images:
            image.image.delete()

    def test_can_add_new_item_to_cart(self):
        variant = ProductVariant.objects.get(pk=1)
        self.client.post(
            reverse("add_to_cart"),
            {
                "variant": variant.id,
                "quantity": 1,
                "drawing": 0,
                "redirect_url": reverse("view_cart"),
            },
        )
        self.assertEqual(
            self.client.session.get("cart"),
            [{"variant_id": "1", "drawing": "0", "quantity": 1}],
        )

    def test_can_increase_item_quantity_in_cart(self):
        # add item to session cart with quantity 1
        session = self.client.session
        session["cart"] = [{"variant_id": "1", "drawing": "0", "quantity": 1}]
        session.save()
        variant = ProductVariant.objects.get(pk=1)
        self.client.post(
            reverse("add_to_cart"),
            {
                "variant": variant.id,
                "quantity": 1,
                "drawing": 0,
                "redirect_url": reverse("view_cart"),
            },
        )
        self.assertEqual(
            self.client.session.get("cart"),
            [{"variant_id": "1", "drawing": "0", "quantity": 2}],
        )


class TestUpdateCartItemView(TestCase):
    """
    Tests that the update_cart_item view is behaving as expected.
    """

    def setUp(self):
        # create a test user
        self.test_user = User.objects.create_user(
            username="testuser", password="123456"
        )
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

        # create a Product
        product = Product.objects.create(
            image=product_image,
            name="test_product",
            display_name="Test Product",
            description="A product for testing",
            variant_type="CL",
        )

        ProductVariant.objects.create(
            product=product,
            display_name="Test Variant",
            name="test_variant",
            price=Decimal(1.99),
            sku="TEST-1",
        )

    def tearDown(self):
        # delete all images from filesystem after running tests
        images = ProductImage.objects.all()
        for image in images:
            image.image.delete()

    def test_can_update_item_quantity_in_cart(self):
        # add item to session cart with quantity 10
        session = self.client.session
        session["cart"] = [{"variant_id": "1", "drawing": "0", "quantity": 10}]
        session.save()
        variant = ProductVariant.objects.get(pk=1)
        # update quantity to 5
        self.client.post(
            reverse("update_cart_item"),
            {
                "variant_id": variant.id,
                "quantity": 5,
                "drawing": 0,
            },
        )
        self.assertEqual(
            self.client.session.get("cart"),
            [{"variant_id": "1", "drawing": "0", "quantity": 5}],
        )

    def test_can_remove_item_from_cart(self):
        # add item to session cart with quantity 10
        session = self.client.session
        session["cart"] = [{"variant_id": "1", "drawing": "0", "quantity": 10}]
        session.save()
        variant = ProductVariant.objects.get(pk=1)
        # update quantity to 0
        self.client.post(
            reverse("update_cart_item"),
            {
                "variant_id": variant.id,
                "quantity": 0,
                "drawing": 0,
            },
        )
        self.assertEqual(self.client.session.get("cart"), [])


class TestRemoveCartItemView(TestCase):
    """
    Tests that the remove_cart_item view is behaving as expected.
    """

    def setUp(self):
        # create a test user
        self.test_user = User.objects.create_user(
            username="testuser", password="123456"
        )

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

        # create a Product
        product = Product.objects.create(
            image=product_image,
            name="test_product",
            display_name="Test Product",
            description="A product for testing",
            variant_type="CL",
        )

        ProductVariant.objects.create(
            product=product,
            display_name="Test Variant",
            name="test_variant",
            price=Decimal(1.99),
            sku="TEST-1",
        )

    def tearDown(self):
        # delete all images from filesystem after running tests
        images = ProductImage.objects.all()
        for image in images:
            image.image.delete()

    def test_can_remove_item_from_cart(self):
        session = self.client.session
        session["cart"] = [{"variant_id": "1", "drawing": "0", "quantity": 5}]
        session.save()
        variant = ProductVariant.objects.get(pk=1)
        self.client.post(
            reverse("remove_cart_item"),
            {
                "variant_id": variant.id,
                "drawing": 0,
            },
        )
        self.assertEqual(self.client.session.get("cart"), [])

    def test_only_selected_item_removed(self):
        session = self.client.session
        session["cart"] = [
            {"variant_id": "1", "drawing": "0", "quantity": 5},
            {"variant_id": "2", "drawing": "0", "quantity": 5},
            {"variant_id": "1", "drawing": "1", "quantity": 5},
            {"variant_id": "2", "drawing": "1", "quantity": 5},
        ]
        session.save()
        variant = ProductVariant.objects.get(pk=1)
        self.client.post(
            reverse("remove_cart_item"),
            {
                "variant_id": variant.id,
                "drawing": 0,
            },
        )
        self.assertEqual(
            self.client.session.get("cart"),
            [
                {"variant_id": "2", "drawing": "0", "quantity": 5},
                {"variant_id": "1", "drawing": "1", "quantity": 5},
                {"variant_id": "2", "drawing": "1", "quantity": 5},
            ],
        )
