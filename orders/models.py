import random
from django.db import models
from cafe.models import Item, Table
# from accounts.models import Customer
# from accounts.models import User
from django.contrib.sessions.models import Session
from accounts.models import TimeStampedModel
from accounts.models import User
from django.contrib.postgres.fields import JSONField
# from django.contrib.sessions.models import Session

# class CustomSession(models.Model):
#     session = models.OneToOneField(Session, primary_key=True, on_delete=models.CASCADE)
#     custom_data = models.TextField()


class Order(TimeStampedModel):
    """
    Represents an order in the cafe application.

    Attributes:
        description (str): The description of the order.
        order_date (datetime): The date and time when the order was placed.
        table_number (int): The number of the table where the order was placed.
        staff_id (str): The ID of the staff member who took the order.
        order_detail (dict): The details of the order in JSON format.
        order_id (str): The ID of the order.
        customer_name (str): The name of the customer who placed the order.
        phone_number (str): The phone number of the customer.
        table_number (int): The number of the table where the order was placed.
        discount_code (str): The discount code applied to the order.
        final_price (str): The final price of the order.
        order_status (bool): The payment status of the order.

    """
    description= models.CharField(verbose_name="توضیحات", max_length=500, null=True , blank=True)
    order_date = models.DateTimeField(verbose_name="زمان ثبت سفارش", auto_now_add=True ,null=True)
    staff_id= models.CharField(verbose_name="شماره کارمند",null=True,blank=True)
    order_detail= models.JSONField(default=dict) #save like dictionary
    order_id= models.CharField(max_length=255)
    customer_name= models.CharField(verbose_name="نام مشتری",blank = True , null = True , max_length=255) 
    phone_number = models.CharField(verbose_name="شماره تلفن",blank = True , null = True , max_length=11) 
    table_number= models.ForeignKey(Table, to_field="table_number", db_column="table_number", on_delete=models.CASCADE)
    discount_code=models.CharField(verbose_name="کد تخفیف ",max_length=255 , null=True , blank=True)
    final_price= models.CharField(max_length=255)
    order_status = models.BooleanField(verbose_name="پرداخت شده", default=False)


    class Meta:
        verbose_name_plural = 'سفارشات'

    def __str__(self) -> str:
        """
        Returns a string representation of the order.

        Returns:
            str: A truncated description of the order.

        """
        return f"{self.description[:20]}..."
  




    




class Discount(models.Model):
    """
    Represents a discount in the cafe application.

    Attributes:
        code (str): The code of the discount.
        percentage (int): The percentage value of the discount.
        start_date (date): The start date of the discount.
        end_date (date): The end date of the discount.

    """
    code = models.CharField(max_length=20, unique=True)
    percentage = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def is_valid(self):
        """
        Checks if the discount is valid.

        Returns:
            bool: True if the discount is valid, False otherwise.

        """
        from django.utils import timezone
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date

    def apply_discount(self, amount):
        """
        Applies the discount to the given amount.

        Args:
            amount (float): The amount to apply the discount to.

        Returns:
            float: The discounted amount.

        """
        if self.is_valid():
            discount_amount = (self.percentage / 100) * amount
            return amount - discount_amount
        else:
            return amount

