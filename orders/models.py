from django.db import models
from cafe.models import Item
# from accounts.models import Customer
# from accounts.models import User
from django.contrib.sessions.models import Session
from accounts.models import TimeStampedModel
from accounts.models import User
from django.contrib.postgres.fields import JSONField


import random

class Order(TimeStampedModel):
    description= models.CharField(verbose_name="توضیحات", max_length=500, null=True , blank=True)
    order_date = models.DateTimeField(verbose_name="زمان ثبت سفارش", auto_now_add=True ,null=True)
    table_number = models.IntegerField(verbose_name="شماره میز", null = True)
    staff_id= models.ForeignKey(User , on_delete=models.CASCADE)
    order_detail= models.JSONField(default=dict) #save like dictionary
    order_id= models.CharField(max_length=255,null=True)
    customer_name = models.CharField(verbose_name="نام مشتری",blank = True , null = True , max_length=255) 
    phone_number = models.CharField(verbose_name="شماره تلفن",blank = True , null = True , max_length=11) 
    table_number= models.IntegerField(verbose_name=" شماره میز ",null=True)
    discount_code=models.CharField(verbose_name="کد تخفیف ",max_length=255 , null=True , blank=True)
    final_price= models.CharField(max_length=255,null=True)
    order_status = models.BooleanField(verbose_name="پرداخت شده", default=False)

    class Meta:
        verbose_name_plural = 'سفارشات'

    def __str__(self) -> str:
        return f"{self.description[:20]}..."
  



# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     item = models.ForeignKey(Item, on_delete=models.CASCADE)
#     quantity = models.IntegerField()
    




class Discount (models.Model):
    code = models.CharField()
    amount= models.IntegerField()
    expired_time= models.DateTimeField(auto_now_add=True)

