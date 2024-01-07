from django import forms


class CartAddForm(forms.Form):
    quantity = forms.CharField(initial=0)
    item_id=forms.CharField()
    action=forms.CharField()
    

class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"جست و جو محصولات"}))