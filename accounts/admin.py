from django.contrib import admin
from orders.models import Bill,Item,Order
from accounts.models import Staff , Customer

admin.site.register(Bill)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Staff)
admin.site.register(Customer)
