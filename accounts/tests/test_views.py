import tempfile
from PIL import Image

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from accounts.models import Drawing


class TestProfileView(TestCase):
    """
    Tests that the profile view is behaving as expected.
    """

    def setUp(self):
        # create a test user
        self.test_user = User.objects.create_user(
            username="testuser", password="123456"
        )

    def test_redirects_if_not_logged_in(self):
        response = self.client.get(reverse("profile"))
        self.assertRedirects(response, "/account/login/?next=/account/")
        self.assertEqual(response.status_code, 302)

    def test_get_profile_page(self):
        self.client.login(username="testuser", password="123456")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/profile.html")

    def test_post_to_profile_page(self):
        self.client.login(username="testuser", password="123456")
        response = self.client.post(reverse("profile"))
        self.assertEqual(response.status_code, 200)


class TestSaveDrawingView(TestCase):
    """
    Tests that the save_drawing view is behaving as expected.
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
                save_slot=2,
                user_account=self.test_user.useraccount,
                image=SimpleUploadedFile(
                    name="test_image.png",
                    content=temp_file.read(),
                ),
            )

    def tearDown(self):
        # delete all images from filesystem after running tests
        drawings = Drawing.objects.all()
        for drawing in drawings:
            drawing.image.delete()

    def test_redirects_if_not_logged_in(self):
        response = self.client.get(reverse("save_drawing"))
        self.assertRedirects(
            response, "/account/login/?next=/account/save_drawing/"
        )
        self.assertEqual(response.status_code, 302)

    def test_400_error_if_form_invalid(self):
        self.client.login(username="testuser", password="123456")
        response = self.client.post(
            reverse("save_drawing"),
            {},
            **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"},
        )
        self.assertEqual(response.status_code, 400)

    def test_can_save_drawings(self):
        self.client.login(username="testuser", password="123456")
        with tempfile.NamedTemporaryFile(suffix=".jpg") as temp_file:
            temp_image = Image.new("RGB", (10, 10))
            temp_image.save(temp_file, format="JPEG")
            temp_file.seek(0)

            # post ajax request with attached image and data
            response = self.client.post(
                reverse("save_drawing"),
                {
                    "title": "Test Drawing",
                    "save_slot": 1,
                    "user_account": self.test_user.useraccount.pk,
                    "image": SimpleUploadedFile(
                        name="test_image.png",
                        content=temp_file.read(),
                    ),
                },
                **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"},
            )

        # find the added object
        drawing = Drawing.objects.filter(title="Test Drawing")[0]

        self.assertEqual(response.status_code, 200)
        self.assertEqual("Test Drawing", drawing.title)

    def test_can_overwrite_drawings(self):
        self.client.login(username="testuser", password="123456")

        # find the drawing saved in the database with save_slot=2
        saved_drawing = Drawing.objects.filter(save_slot=2)[0]
        saved_drawing_id = saved_drawing.id

        with tempfile.NamedTemporaryFile(suffix=".jpg") as temp_file:
            temp_image = Image.new("RGB", (10, 10))
            temp_image.save(temp_file, format="JPEG")
            temp_file.seek(0)
            # post ajax request with save_slot=2
            response = self.client.post(
                reverse("save_drawing"),
                {
                    "title": "New Test Drawing",
                    "save_slot": 2,
                    "user_account": self.test_user.useraccount.pk,
                    "image": SimpleUploadedFile(
                        name="test_image.png",
                        content=temp_file.read(),
                    ),
                },
                **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"},
            )

        # find the added object
        new_drawing = Drawing.objects.filter(save_slot=2)[0]

        self.assertEqual(response.status_code, 200)
        # the new drawing's id should match the saved drawing's id
        self.assertEqual(saved_drawing_id, new_drawing.id)


class TestGetDrawingView(TestCase):
    """
    Tests that the get_drawing view is behaving as expected.
    """

    def setUp(self):
        self.test_user = User.objects.create_user(
            username="testuser", password="123456"
        )
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

    def tearDown(self):
        drawings = Drawing.objects.all()
        for drawing in drawings:
            drawing.image.delete()

    def test_redirects_if_not_logged_in(self):
        response = self.client.get(reverse("get_drawing"))
        self.assertRedirects(
            response, "/account/login/?next=/account/get_drawing/"
        )
        self.assertEqual(response.status_code, 302)

    def test_can_get_drawing(self):
        self.client.login(username="testuser", password="123456")
        response = self.client.get(
            reverse("get_drawing") + "?save_slot=1",
            **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"},
        )
        self.assertIn("url", response.json())
        self.assertEqual(200, response.status_code)

    def test_404_status_if_drawing_not_found(self):
        self.client.login(username="testuser", password="123456")
        response = self.client.get(
            reverse("get_drawing") + "?save_slot=2",
            **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"},
        )
        self.assertEqual(404, response.status_code)


class TestDeleteDrawingView(TestCase):
    """
    Tests that the delete_drawing view is behaving as expected.
    """

    def setUp(self):
        # create two test users
        self.test_user = User.objects.create_user(
            username="testuser", password="123456"
        )
        self.test_user_2 = User.objects.create_user(
            username="testuser2", password="123456"
        )
        with tempfile.NamedTemporaryFile(suffix=".jpg") as temp_file:
            temp_image = Image.new("RGB", (10, 10))
            temp_image.save(temp_file, format="JPEG")
            temp_file.seek(0)

            Drawing.objects.create(
                title="Saved Test Drawing",
                save_slot=2,
                user_account=self.test_user.useraccount,
                image=SimpleUploadedFile(
                    name="test_image.png",
                    content=temp_file.read(),
                ),
            )

    def tearDown(self):
        drawings = Drawing.objects.all()
        for drawing in drawings:
            drawing.image.delete()

    def test_redirects_if_not_logged_in(self):
        drawing = Drawing.objects.get(pk=1)
        url = reverse("delete_drawing", args=(drawing.id,))
        response = self.client.get(url)
        self.assertRedirects(
            response,
            f"/account/login/?next=/account/delete_drawing/{drawing.id}/",
        )
        self.assertEqual(response.status_code, 302)

    def test_404_status_if_drawing_not_found(self):
        self.client.login(username="testuser", password="123456")
        url = reverse("delete_drawing", args=(2,))
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)

    def test_redirects_if_not_drawing_owner(self):
        drawing = Drawing.objects.get(pk=1)
        url = reverse("delete_drawing", args=(drawing.id,))
        self.client.login(username="testuser2", password="123456")
        response = self.client.get(url)
        self.assertRedirects(response, reverse("profile"))
        self.assertEqual(response.status_code, 302)

        # drawing should still exist
        drawing_exists = Drawing.objects.filter(id=drawing.id).first()
        self.assertTrue(drawing_exists)

    def test_can_delete_drawing(self):
        drawing = Drawing.objects.get(pk=1)
        url = reverse("delete_drawing", args=(drawing.id,))
        self.client.login(username="testuser", password="123456")
        response = self.client.get(url)
        self.assertRedirects(response, reverse("profile"))
        self.assertEqual(response.status_code, 302)

        # drawing should not exist
        drawing_exists = Drawing.objects.filter(id=drawing.id).first()
        self.assertFalse(drawing_exists)
