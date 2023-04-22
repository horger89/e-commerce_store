from django import forms
from . models import Order

class OrderForm(forms.ModelForm):

    address_line_2 = forms.CharField(required=False)
    order_note = forms.CharField(required=False)

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2', 'country', 'state', 'city', 'order_note'] 