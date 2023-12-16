from django.db import models


class Menu(models.Model):
    # menu_id = models.AutoField(primary_key=True)
    menu_name = models.CharField(max_length=255)
    description = models.TextField()

class Category(models.Model):
    # category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)

class Item(models.Model):
    # item_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
