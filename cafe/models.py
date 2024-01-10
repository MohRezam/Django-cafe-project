from django.db import models
from accounts.models import TimeStampedModel
from django.core.exceptions import ValidationError

class Menu(models.Model):
    menu_name = models.CharField(max_length=255)
    description = models.TextField()

class Category(models.Model):
    category_name = models.CharField(verbose_name="دسته بندی", max_length=255, unique=True)
    image = models.ImageField(verbose_name="تصویر", upload_to="categories/%Y/%m/%d/")
    
    
    class Meta:  
        verbose_name_plural = 'دسته بندی محصولات'
    
    def __str__(self) -> str:
        return f"دسته بندی: {self.category_name}"

class Item(TimeStampedModel):
    name = models.CharField(verbose_name="محصول", max_length=255)
    price = models.IntegerField(verbose_name="قیمت")
    image = models.ImageField(verbose_name="تصویر", upload_to="items/%Y/%m/%d/")
    description = models.TextField(verbose_name="توضیحات")
    category = models.ForeignKey(Category, verbose_name="دسته بندی", to_field="category_name", on_delete=models.CASCADE)
    ingredients = models.TextField(verbose_name="محتویات")
    item_status = models.BooleanField(verbose_name="موجود", default=True)
    
    class Meta:  
        verbose_name_plural = 'محصولات'
    
    def __str__(self) -> str:
        return f"{self.name}"
class Order(models.Model):
    """
    Represents a table in the cafe.
    """
    CHOICES = (
         ("1", "1"), 
    ("2", "2"), 
    ("3", "3"), 
    ("4", "4"), 
    ("5", "5"), 
    ("6", "6"), 
    ("7", "7"), 
    ("8", "8"),
    ("9", "9"),
    ("10", "10") 
    )
    table_number = models.CharField(verbose_name="شماره میز",choices=CHOICES, unique=True)
    is_available = models.BooleanField(verbose_name="موجود", default=True)

    def __str__(self):
        # return f"Table {self.table_number} - {'Available' if self.is_available else 'Not Available'}"
        return f"{self.table_number} {'' if self.is_available else 'رزرو شده'}"


    class Meta:
        
        verbose_name_plural = 'میز'
    
class Cafe(models.Model):
    name = models.CharField(verbose_name="نام", max_length=100)
    logo_image = models.ImageField(verbose_name="تصویر لوگو", upload_to="cafe/%Y")
    about_page_image = models.ImageField(verbose_name="تصویر صفحه توضیحات", upload_to="cafe/%Y")
    about_page_description = models.TextField(verbose_name="توضیحات")
    address = models.TextField(verbose_name="آدرس")
    phone_number = models.CharField(verbose_name="شماره تماس", max_length=11)
    
    class Meta:
        verbose_name_plural = 'کافه'
        
        
    def save(self, *args, **kwargs):
        if not self.pk and Cafe.objects.exists():
            raise ValidationError('There is can be only one JuicerBaseSettings instance')
        return super(Cafe, self).save(*args, **kwargs)
        
        
    def __str__(self) -> str:
        return self.name