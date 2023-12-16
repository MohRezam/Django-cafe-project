from django.db import models
# from orders import models as orders_models
role_list=(("Barista","Barista") ,('manager', 'Manager') , ("Cashier","Cashier"), ('waiter', 'Waiter'), ("Kitchen Staff","Kitchen Staff"))


class Staff(models.Model):
    # staff_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True)
    phone_number = models.IntegerField()
    role = models.CharField(max_length=255, choices=role_list)