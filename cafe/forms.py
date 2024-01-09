from django import forms


class CartAddForm(forms.Form):
    quantity = forms.CharField(initial=0,widget=forms.TextInput(attrs={"class":"quantity-button"}))
    item_id=forms.CharField()
    action=forms.CharField()
    

class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control form-search", "placeholder":"جست و جو محصولات"}))