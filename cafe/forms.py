from django import forms


class CartAddForm(forms.Form):
    """
    A form for adding items to the cart.
    
    Fields:
    - quantity: The quantity of the item to be added.
    - item_id: The ID of the item to be added.
    - action: The action to be performed (e.g., add, remove, update).
    """
    quantity = forms.CharField(initial=0)
    item_id=forms.CharField()
    action=forms.CharField()
    

class SearchForm(forms.Form):
    """
    A form for searching products.
    
    Fields:
    - search: The search query entered by the user.
    """
    search = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"جست و جو محصولات"}))