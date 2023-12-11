from django.db import models

class Order(models.Model):
    order_number=models.AutoField(primary_key=True)
    # item_id=models.ForeignKey(Item)
    description= models.CharField(max_length=500)
    date= models.DateField(auto_now_add=True)
    time= models.TimeField(auto_now_add=True)
    quantity=models.IntegerField()

class Item(models.Model):
    item_id=models.AutoField(primary_key=True)
    order_id=models.ForeignKey(Order , on_delete= models.CASCADE )
    item_name=models.CharField(max_length=50)
    quantity=models.IntegerField()
    item_cost=models.IntegerField()
    description=models.CharField(max_length=500)

class Bill (models.Model):
    bill_number=models.AutoField(primary_key=True)
    total=models.IntegerField()
    description=models.CharField(max_length=500)
    date=models.DateField(auto_now_add=True)
    time=models.TimeField(auto_now_add=True)
