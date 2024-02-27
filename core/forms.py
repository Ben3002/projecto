from django import forms
from .models import Review

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']


class CheckoutForm(forms.Form):
    billing_address = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_zip = forms.CharField(required=False)

    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_zip = forms.CharField(required=False)

    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
    






