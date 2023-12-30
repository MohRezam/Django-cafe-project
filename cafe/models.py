from django.db import models
from accounts.models import TimeStampedModel


class Menu(models.Model):
    menu_name = models.CharField(max_length=255)
    description = models.TextField()

class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    
    
    class Meta:  
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self) -> str:
        return f"Category: {self.category_name}"

class Item(TimeStampedModel):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(Category, to_field="category_name", on_delete=models.CASCADE)
    ingredients = models.TextField()
    item_status = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return f"Item: {self.name}"
class Table(models.Model):
    table_number = models.IntegerField(unique=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Table {self.table_number} - {'Available' if self.is_available else 'Not Available'}"
