from django import forms


class CartAddForm(forms.Form):
    quantity = forms.CharField()
    iditem=forms.CharField()
    

class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"جست و جو محصولات"}))