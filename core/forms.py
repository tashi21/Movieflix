"""Forms"""
from django import forms
from django_countries.fields import CountryField


class CheckoutForm(forms.Form):
    """Checkout Form"""
    address1 = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "1234 Main St",
        "class": "form-control",
    }))
    address2 = forms.CharField(required=False, widget=forms.TextInput(attrs={
        "placeholder": "Apartment or suite",
        "class": "form-control",
    }))
    country = CountryField().formfield(widget=forms.Select(attrs={
        "class": "form-select",
    }))
    pincode = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "000000",
    }))
    set_default = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)
    PAYMENT_CHOICES = (
        ("C", "Credit Card"),
        ("D", "Debit Card"),
        ("U", "UPI"),
        ("COD", "Cash On Delivery"),
    )
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={
            "class": "custom-control-label",
        }), choices=PAYMENT_CHOICES)
