from django.contrib import admin
from orders.models import Item,Order
from accounts.models import Staff

admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Staff)

