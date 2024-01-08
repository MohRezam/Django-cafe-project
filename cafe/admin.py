from django.contrib import admin
from .models import Menu, Category, Item, Cafe
# Register your models here.
"""
This file is responsible for registering models with the Django admin site.
"""
# admin.site.register(Menu)
admin.site.register(Category) # Register the Category model with the admin site.
admin.site.register(Item) # Register the Item model with the admin site.
admin.site.register(Cafe)  # Register the Cafe model with the admin site.