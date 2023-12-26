from django.db import models
from cafe.models import Item
# from accounts.models import Customer
# from accounts.models import User
from django.contrib.sessions.models import Session
from accounts.models import TimeStampedModel


class Order(TimeStampedModel):
    description= models.CharField(max_length=500)
    order_date = models.DateTimeField(auto_now_add=True ,null=True)
    table_number = models.IntegerField(null = True)
    session = models.OneToOneField(Session, on_delete=models.CASCADE)
    # define a foriegn key to staff id and it should be unique
    
    def __str__(self) -> str:
        return f"{self.description[:20]}..."

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    



# class history(models.Model):
#     phone_number=models.CharField(max_length=11)
#     order_id=models.IntegerField()
    
