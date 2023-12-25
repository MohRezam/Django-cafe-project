from django import forms
from .models import User
from cafe.models import Category
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


# admin panel
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="confirm password", widget=forms.PasswordInput)
    
    
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name')
    
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password1"] and cd["password2"] and cd["password1"] != cd['password2']:
            raise ValidationError("passwords don't match")
        return cd["password2"]
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
   
   
# admin panel 
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text="you can change password using <a href=\"../password/\">this form.</a>")
    
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name', 'password', 'last_login')
        
        

# template 
class UserLoginForm(forms.Form):
    phone_number = forms.CharField(max_length=11)
    password = forms.CharField(widget=forms.PasswordInput)
    # email = forms.EmailField(widget=forms.EmailInput(attrs={"palceholder":"Enter your email"}))

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
