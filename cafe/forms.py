from django import forms


class CartAddForm(forms.Form):
    quantity = forms.CharField()
    iditem=forms.CharField()