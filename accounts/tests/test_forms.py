from django.contrib.auth.models import User
from django.test import TestCase

from accounts.forms import DefaultAddressForm, DrawingForm, NameUpdateForm


class TestNameUpdateForm(TestCase):
    """
    Tests that the NameUpdateForm is behaving as expected.
    """

    def test_correct_fields_are_specified_in_form_meta(self):
        form = NameUpdateForm()
        self.assertEqual(form.Meta.fields, ("first_name", "last_name"))

    def test_no_fields_are_required(self):
        form = NameUpdateForm({"first_name": "", "last_name": ""})
        self.assertTrue(form.is_valid())


class TestDefaultAddressForm(TestCase):
    """
    Tests that the DefaultAddressForm is behaving as expected.
    """

    def test_correct_fields_are_specified_in_form_meta(self):
        form = DefaultAddressForm()
        self.assertEqual(
            form.Meta.fields,
            (
                "default_address_1",
                "default_address_2",
                "default_town",
                "default_county",
                "default_postcode",
                "default_country",
                "default_phone_number",
            ),
        )

    def test_custom_labels_are_applied(self):
        form = DefaultAddressForm()
        self.assertEqual(form.fields["default_address_1"].label, "Address 1")
        self.assertEqual(form.fields["default_address_2"].label, "Address 2")
        self.assertEqual(form.fields["default_town"].label, "Town")
        self.assertEqual(form.fields["default_county"].label, "County")
        self.assertEqual(form.fields["default_postcode"].label, "Postcode")
        self.assertEqual(form.fields["default_country"].label, "Country")

    def test_no_fields_are_required(self):
        data = {
            "default_address_1": "",
            "default_address_2": "",
            "default_town": "",
            "default_county": "",
            "default_postcode": "",
            "default_country": "",
        }

        form = DefaultAddressForm(data)
        self.assertTrue(form.is_valid())


class TestDrawingForm(TestCase):
    """
    Tests that the DrawingForm is behaving as expected.
    """

    def setUp(self):
        # create a test user
        self.test_user = User.objects.create_user(
            username="testuser", password="123456"
        )

    def test_correct_fields_are_specified_in_form_meta(self):
        form = DrawingForm()
        self.assertEqual(form.Meta.fields, ("title", "image", "save_slot"))

    def test_correst_fields_are_required(self):
        data = {}
        file_data = {}
        form = DrawingForm(data, file_data)
        self.assertFalse(form.is_valid())
        self.assertIn("image", form.errors.keys())
        self.assertIn("save_slot", form.errors.keys())
        self.assertNotIn("title", form.errors.keys())
