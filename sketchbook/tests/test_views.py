import tempfile
from PIL import Image

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from accounts.models import Drawing
from prompts.models import Adjective, Creature, Activity, Location


class TestSketchbookView(TestCase):
    """
    Tests that the Drawing model is behaving as expected.
    """

    def setUp(self):
        # create a test user
        self.test_user = User.objects.create_user(
            username="testuser", password="123456"
        )

        # create a test drawing object with a title
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

        # create a test drawing object without a title
        with tempfile.NamedTemporaryFile(suffix=".jpg") as temp_file:
            temp_image = Image.new("RGB", (10, 10))
            temp_image.save(temp_file, format="JPEG")
            temp_file.seek(0)

            Drawing.objects.create(
                title="",
                save_slot=2,
                user_account=self.test_user.useraccount,
                image=SimpleUploadedFile(
                    name="test_image.png",
                    content=temp_file.read(),
                ),
            )

        # create some words for the prompt generation functions
        Adjective.objects.create(
            adjective="adjective",
            determiner="an",
        )
        Activity.objects.create(
            activity="activity",
        )
        Creature.objects.create(
            creature="creature",
            determiner="a",
            plural="creatures",
        )
        Location.objects.create(
            location="location",
        )

    def tearDown(self):
        # delete all images from filesystem after running tests
        drawings = Drawing.objects.all()
        for drawing in drawings:
            drawing.image.delete()

    def test_get_sketchbook_page(self):
        response = self.client.get(reverse("sketchbook"))
        self.assertEqual(response.status_code, 200)

    def test_logged_out_view_contains_correct_contexts(self):
        response = self.client.get(reverse("sketchbook"))
        self.assertTemplateUsed(response, "sketchbook/sketchbook.html")
        self.assertIsNone(response.context["saved_drawings"])
        self.assertIsNone(response.context["form"])
        self.assertFalse(response.context["titles"])

    def test_logged_in_view_contains_correct_contexts(self):
        self.client.login(username="testuser", password="123456")
        response = self.client.get(reverse("sketchbook"))
        self.assertIsNotNone(response.context["saved_drawings"])
        self.assertIsNotNone(response.context["form"])
        self.assertTrue(response.context["titles"])
        self.assertEqual(
            response.context["titles"]["title_1"], "Saved Test Drawing"
        )
        self.assertEqual(response.context["titles"]["title_2"], "")
