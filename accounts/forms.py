from django import forms
from .models import User
from orders.models import Order
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from cafe.models import Item,Category,Table,Cafe


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

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'image']
        labels = {
            'category_name': 'دسته بندی',
            'image': 'تصویر',
        }

class CategoryChangeForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'image']
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
class SortOrdersPhone(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"جست و جوی سفارش ها"}))        

class ChangeOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['order_date']  
        labels = {
            'description': 'توضیحات',
            'table_number': 'شماره میز',
            'staff_id': 'شماره کارمند',
            'order_detail': 'جزئیات سفارش',
            'order_id': 'شماره سفارش',
            'customer_name': 'نام مشتری',
            'phone_number': 'شماره تلفن',
            'discount_code': 'کد تخفیف',
            'final_price': 'قیمت نهایی',
            'order_status': 'پرداخت شده'
        }
        widgets = {
            'order_detail': forms.Textarea(),  
            'order_status': forms.CheckboxInput(),
        }

class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['order_date']
        labels = {
            'description': 'توضیحات',
            'table_number': 'شماره میز',
            'staff_id': 'شماره کارمند',
            'order_detail': 'جزئیات سفارش',
            'order_id': 'شماره سفارش',
            'customer_name': 'نام مشتری',
            'phone_number': 'شماره تلفن',
            'discount_code': 'کد تخفیف',
            'final_price': 'قیمت نهایی',
            'order_status': 'پرداخت شده'
        }
        widgets = {
            'order_detail': forms.Textarea(),  
            'order_status': forms.CheckboxInput(),  
        }
# template 
class UserLoginForm(forms.Form):
    phone_number = forms.CharField(label="شماره موبایل :",max_length=11)
    password = forms.CharField(label="رمز عبور :",widget=forms.PasswordInput)
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and len(phone_number) != 11:
         raise forms.ValidationError('شماره تلفن باید یازده رقم باشد')
        return phone_number

class TableForm(forms.ModelForm):
    CHOICES = (
        ("1", "1"), 
        ("2", "2"), 
        ("3", "3"), 
        ("4", "4"), 
        ("5", "5"), 
        ("6", "6"), 
        ("7", "7"), 
        ("8", "8"),
        ("9", "9"),
        ("10", "10") 
    )
    
    table_number = forms.ChoiceField(label='شماره میز', choices=CHOICES)
    is_available = forms.BooleanField(label='موجود', required=False)

    class Meta:
        model = Table
        fields = ['table_number', 'is_available']

class CafeForm(forms.ModelForm):
    class Meta:
        model = Cafe
        fields = ['name', 'logo_image', 'about_page_image', 'about_page_description', 'address', 'phone_number', 'instagram_url', 'teleram_url', 'whatsapp_url']
        labels = {
            'name': 'نام',
            'logo_image': 'تصویر لوگو',
            'about_page_image': 'تصویر صفحه توضیحات',
            'about_page_description': 'توضیحات',
            'address': 'آدرس',
            'phone_number': 'شماره تماس',
            'instagram_url': 'URL اینستاگرام',
            'teleram_url': 'URL تلگرام',
            'whatsapp_url': 'URL واتساپ',
        }
        widgets = {
            'about_page_description': forms.Textarea(attrs={'rows': 5}),
        }
