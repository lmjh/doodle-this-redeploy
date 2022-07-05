from django.forms.widgets import ClearableFileInput


class ProductImageInput(ClearableFileInput):
    """
    A custom image uplead widget to provide admins with a preview of the
    drawing overlay
    """
    template_name = 'prints/widget_templates/product_image_input.html'
