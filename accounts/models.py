from django.db import models
from orders import models as orders_models
Role_list=(("Barista","Barista") , ("Cashier","Cashier"), ("Server","Server"), ("Kitchen Staff","Kitchen Staff"),("Cleaner","Cleaner"))


class Manager(models.Model):
    manager_id= models.AutoField(primary_key=True)
    manager_name=models.CharField(max_length=50)
    phone_number=models.IntegerField(max_length=11)

class staffs(models.Model):
    employee_id=models.AutoField(primary_key=True)
    employee_name= models.CharField(max_length=50)
    address= models.CharField(max_length=400)
    phone_number= models.IntegerField(max_length=11)
    # role= models.Choi(Role_lis)
    role = models.CharField(max_length=20, choices=Role_list)
    manager=models.ForeignKey(Manager , on_delete=models.DO_NOTHING)



class Customer(models.Model):
    customer_name=models.CharField(max_length=50)
    phone_number=models.IntegerField(max_length=11)
    address=models.CharField(max_length=400)
    rel=models.OneToOneField(orders_models.Order , on_delete=models.DO_NOTHING )
