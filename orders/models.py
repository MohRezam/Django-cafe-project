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
    description= models.CharField(verbose_name="توضیحات", max_length=500, null=True , blank=True)
    order_date = models.DateTimeField(verbose_name="زمان ثبت سفارش", auto_now_add=True ,null=True)
    staff_id= models.CharField(verbose_name="شماره کارمند",null=True,blank=True)
    order_detail= models.JSONField(default=dict)
    order_id= models.CharField(max_length=255)
    customer_name= models.CharField(verbose_name="نام مشتری",blank = True , null = True , max_length=255) 
    phone_number = models.CharField(verbose_name="شماره تلفن",blank = True , null = True , max_length=11) 
    table_number= models.ForeignKey(Table, to_field="table_number", db_column="table_number", on_delete=models.CASCADE)
    discount_code=models.CharField(verbose_name="کد تخفیف ",max_length=255 , null=True , blank=True)
    final_price= models.IntegerField()
    order_status = models.BooleanField(verbose_name="پرداخت شده", default=False)


    class Meta:
        verbose_name_plural = 'سفارشات'

    def __str__(self) -> str:
        return f"{self.phone_number}"
  




    




class Discount(models.Model):
    code = models.CharField(max_length=20, unique=True)
    percentage = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def is_valid(self):
        from django.utils import timezone
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date

    def apply_discount(self, amount):
        if self.is_valid():
            discount_amount = (self.percentage / 100) * amount
            return amount - discount_amount
        else:
            return amount

