from django.contrib import admin
from .models import Order

"""
Customizes the admin interface for the Order model.
"""

# Register your models here.


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'order_date', 'customer_name', 'table_number', 'order_status')
    list_filter = ('order_status',)
    search_fields = ('order_id', 'customer_name', 'table_number__table_number')