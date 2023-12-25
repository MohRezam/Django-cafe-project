from django import forms


class UserSessionForm(forms.Form):
    phone_number=forms.CharField(max_length=11)

