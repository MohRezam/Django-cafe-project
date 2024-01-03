from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from cafe.models import Item,Category


# admin panel

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['email', 'phone_number', 'full_name', 'address', 'national_id', 'is_active', 'is_admin','password']
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        cleaned_phone_number = User().convert_to_english_numbers(phone_number)
        # Additional validation (e.g., ensuring the length or format of the phone number)
        # For example:
        if len(cleaned_phone_number) != 11:
            raise forms.ValidationError('شماره تلفن باید ۱۱ رقم باشد.')
        
        return cleaned_phone_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Additional email validation if necessary
        return email

   
# admin panel 
class UserChangeForm(forms.ModelForm):    
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name', 'address', 'national_id')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'ایمیل'
        self.fields['phone_number'].label = 'شماره تلفن'
        self.fields['full_name'].label = 'نام و نام خانوادگی'
        self.fields['address'].label = 'آدرس'
        self.fields['national_id'].label = 'کد ملی'
        
        

# template 
class UserLoginForm(forms.Form):
    phone_number = forms.CharField(label="شماره موبایل :",max_length=11)
    password = forms.CharField(label="رمز عبور :",widget=forms.PasswordInput)
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and len(phone_number) != 11:
         raise forms.ValidationError('شماره تلفن باید یازده رقم باشد')
        return phone_number
        


# admin panel
class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        exclude = ['created_at']
        fields = ('category_name', 'image')
        labels = {
            'category_name': 'دسته بندی',
            'image': 'تصویر',
        }
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['created_at']
        fields = ['name', 'price', 'description', 'image', 'category', 'ingredients', 'item_status']
        labels = {
            'name': 'نام محصول',
            'price': 'قیمت',
            'image': 'تصویر',
            'description': 'توضیحات',
            'category': 'دسته بندی',
            'ingredients': 'محتویات',
            'item_status': 'وضعیت موجودی',
        }
        widgets = {
            'image': forms.FileInput(attrs={'type': 'file'}),
        }
    
    