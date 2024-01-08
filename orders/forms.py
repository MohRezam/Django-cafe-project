from django import forms
from .models import Order ,Discount

class OrderForm(forms.ModelForm):
    """
    A form for creating or updating an Order object.
    """
    class Meta:
        model = Order
        fields = ['description', 'table_number', 'customer_name', 'phone_number', 'discount_code']  

class DiscountCodeForm(forms.ModelForm):
    """
    A form for creating or updating a Discount object.
    """
    class Meta:
        model = Discount
        fields = ['code']





class UserSessionForm(forms.Form):
    """
    A form for capturing the user's phone number.
    """
    phone_number=forms.CharField(max_length=11)

class CartAddForm(forms.Form):
    """
    A form for adding items to the cart.
    """
    quantity = forms.CharField()
    item_id=forms.CharField()
    action=forms.CharField()




# class CartEditForm(forms.Form):
#     iditem = forms.IntegerField(widget=forms.HiddenInput())
#     quantity = forms.IntegerField(min_value=1)

#     def clean_quantity(self):
#         quantity = self.cleaned_data['quantity']
#         if quantity < 1:
#             raise forms.ValidationError("Quantity should be greater than or equal to 1.")
#         return quantity