from django.db import models
from cafe.models import Item
# from accounts.models import Customer
# from accounts.models import User
from django.contrib.sessions.models import Session


class Order(models.Model):
    # item_id=models.ForeignKey(Item)
    description= models.CharField(max_length=500)
    order_date = models.DateTimeField(auto_now_add=True ,null=True)
    table_number = models.IntegerField(null = True)
    customer = models.ForeignKey(Session, on_delete=models.CASCADE)
    

class OrderItem(models.Model):
    # order_item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    