from django.db import models
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import EmailValidator
from .managers import UserManager
from django.db import models
from jdatetime import datetime as jdatetime_datetime
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


# Define the role choices for the Staff model
class User(AbstractBaseUser):
    """
    Custom user model.
    """
    email = models.EmailField(max_length=255, unique=True,validators=[EmailValidator()])
    phone_number = models.CharField(max_length=11, unique=True)
    full_name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    national_id = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()
    
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["email", "full_name"]
    
    class Meta:
        verbose_name_plural = 'کارمندان'
    
    def convert_to_english_numbers(self, input_str):
        """
        Convert Persian numbers to English numbers in a given string.
        """
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
    
    def clean_email(self, email):
        """
        Clean and validate the email field.
        """
        return self.email

    def clean_phone_number(self, phone_number):
        """
        Clean and validate the phone_number field.
        """
        cleaned_phone_number = self.convert_to_english_numbers(phone_number)
        # Additional validation (e.g., ensuring the length or format of the phone number)
        # For example:
        if len(cleaned_phone_number) != 11:
            raise ValueError('Phone number should be 11 digits long.')

        return cleaned_phone_number  
    def save(self, *args, **kwargs):
        """
        Override the save method to clean and validate the phone_number and email fields before saving.
        """
        self.phone_number = self.clean_phone_number(self.phone_number)
        self.email = self.clean_email(self.email)
        super().save(*args, **kwargs)    
    def __str__(self):
        """
        Return a string representation of the User object.
        """
        return self.email
    
    def has_perm(self, perm, obj=None):
        """
        Check if the user has a specific permission.
        """
        return True
    
    def has_module_perms(self, app_label):
        """
        Check if the user has permissions to access a specific module.
        """
        return True
    
    @property
    def is_staff(self):
        """
        Check if the user is a staff member.
        """
        return self.is_admin
   

# class TimeStampedModel(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


#     class Meta:
#         abstract = True
#     def save(self, *args, **kwargs):
#     # Update the 'updated_at' timestamp before saving
#         self.updated_at = timezone.now()
#         super(TimeStampedModel, self).save(*args, **kwargs)

class TimeStampedModel(models.Model):
    """
    Abstract base model class that provides created_at and updated_at fields.
    """
    created_at = models.CharField(max_length=20, editable=False)
    updated_at = models.CharField(max_length=20, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Override the save method to update the 'updated_at' timestamp before saving.
        """
        # Update the 'updated_at' timestamp before saving
        self.updated_at = str(jdatetime_datetime.now().strftime('%Y/%m/%d %H:%M:%S'))

        if not self.created_at:
            self.created_at = str(jdatetime_datetime.now().strftime('%Y/%m/%d %H:%M:%S'))

        super(TimeStampedModel, self).save(*args, **kwargs)

# This is an idea, it may add later
# class BaseItem(TimeStampedModel):
#     item_title = models.CharField(max_lengh=50)
#     item_description = models.TextField()
#     item_ingredeint = models.TextField()
    
