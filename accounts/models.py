from django.db import models
# from orders import models as orders_models
Role_list=(("Barista","Barista") , ("Cashier","Cashier"), ("Server","Server"), ("Kitchen Staff","Kitchen Staff"),("Cleaner","Cleaner"))




class Staff(models.Model):
    staff_name= models.CharField(max_length=50)
    address= models.CharField(max_length=400)
    phone_number= models.IntegerField(max_length=11)
    # role= models.Choi(Role_lis)
    role = models.CharField(max_length=20, choices=Role_list)
    # image=models.ImageField()
    date_of_employement=models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"name: {self.staff_name}"



class Customer(models.Model):
    customer_name=models.CharField(max_length=50)
    phone_number=models.IntegerField(max_length=11)
    address=models.CharField(max_length=400)
    # order=models.OneToOneField(orders_models.Order , on_delete=models.DO_NOTHING )
    
    def __str__(self) -> str:
        return f"name: {self.customer_name}"
