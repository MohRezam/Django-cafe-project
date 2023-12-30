from django import forms
from .models import User
from cafe.models import Category
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


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
        self.fields["password"].label = "رمز"
        
        

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
class CategoryForm(forms.Form):
    name = forms.CharField(
        label='نام دسته بندی',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'input-name-checkout',
            'placeholder': 'نام دسته بندی را وارد کنید',
        })
    )   
    def clean_name(self):
        name = self.cleaned_data['name']
        if Category.objects.filter(category_name=name).exists():
            raise forms.ValidationError('این نام دسته بندی قبلاً استفاده شده است.')
        return name

# admin panel      
class AddItemForm(forms.Form):
    name = forms.CharField(label='نام آیتم', max_length=100)
    fixed_number = forms.DecimalField(label='قیمت آیتم')
    category = forms.ChoiceField(
        label='دسته بندی',
        choices=[
            ('date-desc', 'دسته بندی مورد نظر را انتخاب کنید'),
            ('date-asc', 'غذای اصلی'),
            ('rate', 'صبحانه'),
            ('views', 'شام'),
            ('comments', 'عصرانه'),
        ]
    )
    description = forms.CharField(
        label='توضیحات آیتم',
        widget=forms.Textarea(attrs={'style': 'height: 80px;'})
    )
    form_file = forms.ImageField(label='افزودن عکس آیتم')


    
    