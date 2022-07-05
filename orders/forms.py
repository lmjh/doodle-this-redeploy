from django import forms
from .models import Order, OrderDrawingCache

# import objects from Crispy Forms to customise form layouts
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field


class OrderForm(forms.ModelForm):
    """
    A form to collect the user's personal details during checkout
    """
    class Meta:
        model = Order
        fields = (
            'first_name',
            'last_name',
            'address_1',
            'address_2',
            'town',
            'county',
            'postcode',
            'country',
            'email_address',
            'phone_number',
        )

    def __init__(self, *args, **kwargs):
        """
        Configure form layout
        """
        super().__init__(*args, **kwargs)

        # create layout helper
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Div(Field("first_name"), css_class="col-12 col-sm-6"),
            Div(Field("last_name"), css_class="col-12 col-sm-6"),
            Field("address_1", css_class="col-12"),
            Field("address_2", css_class="col-12"),
            Div(Field("town"), css_class="col-12 col-sm-6"),
            Div(Field("county"), css_class="col-12 col-sm-6"),
            Div(Field("postcode"), css_class="col-12 col-sm-6"),
            Div(Field("country"), css_class="col-12 col-sm-6"),
            Div(Field("email_address"), css_class="col-12 col-sm-6"),
            Div(Field("phone_number"), css_class="col-12 col-sm-6"),
        )


class OrderDrawingCacheForm(forms.ModelForm):
    """
    A form to save the store the user's current drawing in the database while
    processing payment
    """
    class Meta:
        model = OrderDrawingCache
        fields = ('image', 'stripe_pid')
