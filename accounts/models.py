from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import EmailValidator
from .managers import UserManager
import re
# from orders import models as orders_models
# role_list=(("Barista","Barista") ,('manager', 'Manager') , ("Cashier","Cashier"), ('waiter', 'Waiter'), ("Kitchen Staff","Kitchen Staff"))


# class Staff(models.Model):
#     name = models.CharField(max_length=255, null=True, blank=True)
#     email = models.EmailField(max_length=255, null=True)
#     phone_number = models.CharField(max_length=11)
#     role = models.CharField(max_length=255, choices=role_list)
    
    
# class Customer(models.Model):
#     name = models.CharField(max_length=255)
#     email = models.EmailField(max_length=255)
#     phone_number = models.CharField(max_length=11)


# custom user
class BaseUser(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True,validators=[EmailValidator()])
    phone_number = models.CharField(max_length=11, unique=True)
    full_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["email", "full_name"]
    
    def convert_to_english_numbers(self, input_str):
        persian_to_english = {
            '۰': '0',
            '۱': '1',
            '۲': '2',
            '۳': '3',
            '۴': '4',
            '۵': '5',
            '۶': '6',
            '۷': '7',
            '۸': '8',
            '۹': '9',
        }

        persian_pattern = re.compile(r'[۰-۹]')

        english_number_str = persian_pattern.sub(lambda x: persian_to_english[x.group()], input_str)

        return english_number_str

    def clean_phone_number(self, phone_number):
        cleaned_phone_number = self.convert_to_english_numbers(phone_number)
        # Additional validation (e.g., ensuring the length or format of the phone number)
        # For example:
        if len(cleaned_phone_number) != 11:
            raise ValueError('Phone number should be 11 digits long.')

        return cleaned_phone_number  
    def save(self, *args, **kwargs):
        self.phone_number = self.clean_phone_number(self.phone_number)
        self.email = self.clean_email(self.email)
        super().save(*args, **kwargs)    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
    
