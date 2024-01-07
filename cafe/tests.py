from django.test import TestCase
from .models import Menu, Category, Item, Table, Cafe
from django.core.exceptions import ValidationError
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.messages import get_messages
from .models import Cafe, Item
from .views import *
#models test
class MenuModelTestCase(TestCase):
    def test_menu_model_fields(self):
        menu = Menu.objects.create(menu_name='Breakfast Menu', description='A selection of breakfast items')
        self.assertEqual(menu.menu_name, 'Breakfast Menu')
        self.assertEqual(menu.description, 'A selection of breakfast items')

class CategoryModelTestCase(TestCase):
    def test_category_model_fields(self):
        category = Category.objects.create(category_name='Drinks', image='path/to/image.jpg')
        self.assertEqual(category.category_name, 'Drinks')
        self.assertEqual(category.image, 'path/to/image.jpg')

    def test_category_str_representation(self):
        category = Category.objects.create(category_name='Desserts', image='path/to/image.jpg')
        self.assertEqual(str(category), 'دسته بندی: Desserts')

class ItemModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(category_name='Drinks', image='path/to/image.jpg')

    def test_item_model_fields(self):
        item = Item.objects.create(name='Coffee', price=5, image='path/to/image.jpg',
                                   description='Freshly brewed coffee', category=self.category,
                                   ingredients='Coffee beans, water', item_status=True)
        self.assertEqual(item.name, 'Coffee')
        self.assertEqual(item.price, 5)
        self.assertEqual(item.description, 'Freshly brewed coffee')
        self.assertEqual(item.category, self.category)
        self.assertEqual(item.ingredients, 'Coffee beans, water')
        self.assertTrue(item.item_status)

    def test_item_str_representation(self):
        item = Item.objects.create(name='Tea', price=3, image='path/to/image.jpg',
                                   description='A cup of tea', category=self.category,
                                   ingredients='Tea leaves, hot water', item_status=True)
        self.assertEqual(str(item), 'محصول: Tea')

class TableModelTestCase(TestCase):
    def test_table_model_fields(self):
        table = Table.objects.create(table_number=1, is_available=True)
        self.assertEqual(table.table_number, 1)
        self.assertTrue(table.is_available)

    def test_table_str_representation(self):
        table = Table.objects.create(table_number=2, is_available=False)
        self.assertEqual(str(table), 'Table 2 - Not Available')

class CafeModelTestCase(TestCase):
    def test_cafe_model_fields(self):
        cafe = Cafe.objects.create(name='Cafe Name', logo_image='path/to/logo.jpg',
                                   about_page_image='path/to/about.jpg', about_page_description='About the cafe',
                                   address='Cafe Address', phone_number='12345678901')
        self.assertEqual(cafe.name, 'Cafe Name')
        self.assertEqual(cafe.logo_image, 'path/to/logo.jpg')
        self.assertEqual(cafe.about_page_image, 'path/to/about.jpg')
        self.assertEqual(cafe.about_page_description, 'About the cafe')
        self.assertEqual(cafe.address, 'Cafe Address')
        self.assertEqual(cafe.phone_number, '12345678901')

    def test_cafe_str_representation(self):
        cafe = Cafe.objects.create(name='Test Cafe', logo_image='path/to/logo.jpg',
                                   about_page_image='path/to/about.jpg', about_page_description='About the test cafe',
                                   address='Test Cafe Address', phone_number='12345678901')
        self.assertEqual(str(cafe), 'Test Cafe')

    def test_single_cafe_instance(self):
        Cafe.objects.create(name='Unique Cafe', logo_image='path/to/logo.jpg',
                            about_page_image='path/to/about.jpg', about_page_description='Unique cafe description',
                            address='Unique Cafe Address', phone_number='12345678901')
        with self.assertRaises(ValidationError):
            Cafe.objects.create(name='Duplicate Cafe', logo_image='path/to/logo.jpg',
                                about_page_image='path/to/about.jpg', about_page_description='Duplicate cafe description',
                                address='Duplicate Cafe Address', phone_number='12345678901')

