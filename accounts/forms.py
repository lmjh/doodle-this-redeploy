from django import forms
from django.contrib.auth.models import User

# import objects from Crispy Forms to customise form layouts
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field

from .models import UserAccount, Drawing


class NameUpdateForm(forms.ModelForm):
    """
    A form to update the first_name and last_name in the current user's User
    model.
    """

    class Meta:
        model = User
        fields = ("first_name", "last_name")

    def __init__(self, *args, **kwargs):
        """
        Configure form layout with crispyforms helper
        """
        super().__init__(*args, **kwargs)

        # create layout helper
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helperdisable_csrf = True
        self.helper.layout = Layout(
            Div(Field("first_name"), css_class="col-12 col-sm-6"),
            Div(Field("last_name"), css_class="col-12 col-sm-6"),
        )


class DefaultAddressForm(forms.ModelForm):
    """
    A form to update the current user's default delivery address details
    """

    class Meta:
        model = UserAccount
        fields = (
            "default_address_1",
            "default_address_2",
            "default_town",
            "default_county",
            "default_postcode",
            "default_country",
            "default_phone_number",
        )

    def __init__(self, *args, **kwargs):
        """
        Replace auto-generated labels and configure form layout
        """
        super().__init__(*args, **kwargs)
        # replace labels
        labels = {
            "default_address_1": "Address 1",
            "default_address_2": "Address 2",
            "default_town": "Town",
            "default_county": "County",
            "default_postcode": "Postcode",
            "default_country": "Country",
            "default_phone_number": "Phone Number",
        }

        # create layout helper
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Field("default_address_1", css_class="col-12"),
            Field("default_address_2", css_class="col-12"),
            Div(Field("default_town"), css_class="col-12 col-sm-6"),
            Div(Field("default_county"), css_class="col-12 col-sm-6"),
            Div(Field("default_postcode"), css_class="col-12 col-sm-6"),
            Div(Field("default_country"), css_class="col-12 col-sm-6"),
            Div(
                Field("default_phone_number"),
                css_class="col-12 col-sm-6 offset-sm-6",
            ),
        )

        # apply custom field labels
        for field in self.fields:
            self.fields[field].label = labels[field]


class DrawingForm(forms.ModelForm):
    """
    A form to save the current user's drawing canvas into the database.
    """

    class Meta:
        model = Drawing
        fields = ("title", "image", "save_slot")
