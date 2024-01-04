from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'phone_number', 'table_number', 'discount_code']

class DiscountCodeForm(forms.Form):
    discount_code = forms.CharField(max_length=255)

class UserSessionForm(forms.Form):
    phone_number=forms.CharField(max_length=11)



# class CartEditForm(forms.Form):
#     iditem = forms.IntegerField(widget=forms.HiddenInput())
#     quantity = forms.IntegerField(min_value=1)

#     def clean_quantity(self):
#         quantity = self.cleaned_data['quantity']
#         if quantity < 1:
#             raise forms.ValidationError("Quantity should be greater than or equal to 1.")
#         return quantity