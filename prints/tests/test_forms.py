import tempfile
from PIL import Image

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from prints.forms import ProductImageForm
from prints.models import ProductImage


class TestProductImageForm(TestCase):
    """
    Tests that the ProductImageForm is behaving as expected.
    """

    def tearDown(self):
        # delete all images from filesystem after running tests
        images = ProductImage.objects.all()
        for image in images:
            image.image.delete()

    def test_correct_fields_are_specified_in_form_meta(self):
        form = ProductImageForm()
        self.assertEqual(form.Meta.fields, ("__all__"))

    def test_users_can_create_product_image(self):
        # build dict for form data
        data = {
            "name_slug": "test_image",
            "image_type": ".jpg",
            "overlay_width": "50%",
            "overlay_x_offset": "10%",
            "overlay_y_offset": "10%",
        }

        # create a temporary file called temp_file
        with tempfile.NamedTemporaryFile(suffix=".jpg") as temp_file:
            # create a new image, mode rgb, 1px x 1px
            temp_image = Image.new("RGB", (1, 1))
            # save the image into the temp file path in jpeg format
            temp_image.save(temp_file, format="JPEG")
            # set the file's current position to the start
            temp_file.seek(0)
            # create a file_data dict using a SimpleUploadedFile object
            file_data = {
                "image": SimpleUploadedFile(
                    name="temp_file.jpg",
                    # read the temp_file into the content attribute
                    content=temp_file.read(),
                )
            }

            # instantiate a ProductImageForm with the data and save
            form = ProductImageForm(data, file_data)
            form.save()

        product_image = ProductImage.objects.filter(name_slug="test_image")
        # form should be valid and object should be found
        self.assertTrue(form.is_valid())
        self.assertEqual(len(product_image), 1)
