from django import forms
from .models import Order ,Discount
from cafe.models import Table
class OrderForm(forms.ModelForm):
    """
    A form for creating or updating an Order object.
    """
    class Meta:
        model = Order
        fields = ['description', 'table_number', 'customer_name', 'phone_number', 'discount_code']  
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['table_number'].queryset = Table.objects.filter(is_available=True)
    
    def clean(self):
        cleaned_data = super().clean()
        chosen_item = cleaned_data.get('table_number')

        if chosen_item:
            chosen_item.is_available = False
            chosen_item.save()

        return cleaned_data

class DiscountCodeForm(forms.ModelForm):
    """
    A form for creating or updating a Discount object.
    """

    class Meta:
        model = Discount
        fields = ['code']
        widgets = {
            'code': forms.TextInput(attrs={'class':'input-coupon w-75','placeholder':'افزودن کد تخفیف'}),   
        }





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