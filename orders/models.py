from django.db import models
from cafe.models import Item
# from accounts.models import Customer
# from accounts.models import User
from django.contrib.sessions.models import Session
from accounts.models import TimeStampedModel


class Order(TimeStampedModel):
    description= models.CharField(verbose_name="توضیحات", max_length=500)
    order_date = models.DateTimeField(verbose_name="زمان ثبت سفارش", auto_now_add=True ,null=True)
    table_number = models.IntegerField(verbose_name="شماره میز", null = True)
    session = models.OneToOneField(Session, on_delete=models.CASCADE)
    # define a foriegn key to staff id and it should be unique
    # define a order_id (this is which we generate it in CafeMenuView )
    
    class Meta:
        verbose_name_plural = 'سفارشات'
    def __str__(self) -> str:
        return f"{self.description[:20]}..."

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    



# class Checkouts(models.Model):
#     discountـcode=models.CharField()
#     name= models.CharField(max_length=250)
#     phone_number=models.CharField(max_length=11)
#     order_id=models.CharField()
#     table_number= models.IntegerField()


# class discount (models.Model):
#     code = models.CharField()
#     amount= models.IntegerField()

