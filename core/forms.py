"""Forms"""
from django import forms
from django_countries.fields import CountryField


class Search(forms.Form):
    """Search form"""
    actor = forms.CharField(max_length=100, required=False)
    director = forms.CharField(max_length=100, required=False)
    genre = forms.CharField(max_length=60, required=False)


class ProfileForm(forms.Form):
    """Profile form"""
    username = forms.CharField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    profile_pic = forms.ImageField(required=False)
    phone_number = forms.CharField(max_length=10, required=False)


class PasswordForm(forms.Form):
    """Password form"""
    password_old = forms.CharField(widget=forms.PasswordInput, required=False)
    password1 = forms.CharField(widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(widget=forms.PasswordInput, required=False)


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
    pincode = forms.CharField(max_length=6, widget=forms.TextInput(attrs={
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
