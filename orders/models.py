from django.db import models
from accounts.models import Staff,Customer

class Bill (models.Model):
   
    total_cost=models.PositiveBigIntegerField()
    description=models.CharField(max_length=500)
    date_time=models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    # item_id=models.ForeignKey(Item)
    description= models.CharField(max_length=500)
    date= models.DateField(auto_now_add=True)
    time= models.TimeField(auto_now_add=True)
    quantity=models.IntegerField()
    staff=models.OneToOneField(to=Staff,to_field="id" , on_delete=models.DO_NOTHING)
    bill=models.OneToOneField(to=Bill,to_field="id" ,on_delete=models.DO_NOTHING)
    customer=models.OneToOneField(to=Customer , to_field="id" , on_delete=models.CASCADE)

class Item(models.Model):
    item_name=models.CharField(max_length=50)
    quantity=models.IntegerField()
    item_cost=models.IntegerField()
    description=models.CharField(max_length=500)
    staff=models.ForeignKey(Staff , on_delete=models.DO_NOTHING)
    order=models.ForeignKey(Order , on_delete= models.CASCADE )


