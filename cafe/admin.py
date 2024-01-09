from django.contrib import admin
from .models import Menu, Category, Item, Cafe, Table

"""
This file is responsible for registering models with the Django admin site.
"""

# Register your models here.


# admin.site.register(Menu)

# @admin.register(Table)
# class TableAdmin(admin.ModelAdmin):
#     list_display = ('table_number', 'is_available')
#     list_filter = ('is_available',)
#     search_fields = ('table_number',)
#     ordering = ('table_number',)
admin.site.register(Table)

@admin.register(Cafe)
class CafeAdmin(admin.ModelAdmin):  # Register the Cafe model with the CafeAdmin.
    list_display = ('name', 'phone_number')
    search_fields = ('name', 'phone_number')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):  # Register the Item model with the ItemAdmin.
    list_display = ('name', 'price', 'category', 'item_status')
    list_filter = ('category', 'item_status')
    search_fields = ('name', 'category__category_name')
    
    

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)
    search_fields = ('category_name',)