from django.contrib import admin
from .models import Order
# Register your models here.
"""
Customizes the admin interface for the Order model.
"""

admin.site.register(Order)
# admin.site.register(OrderItem)