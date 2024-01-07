from django.test import TestCase , Client
from .models import Menu, Category, Item, Table, Cafe
from django.core.exceptions import ValidationError
from django.test import TestCase, RequestFactory
from django.urls import reverse
from cafe.forms import CartAddForm, SearchForm
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.messages import get_messages
from .models import Cafe, Item
from .views import *
from cafe.views import *
from . import views
from . import urls
from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from cafe.admin import Category, Item, Cafe
from cafe.models import Category, Item

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
#urls test
# class TestURLPatterns(TestCase):

#     def test_home_url(self):
#         url = reverse('home')
#         self.assertEqual(url, '/')

#     def test_about_url(self):
#         url = reverse('about')
#         self.assertEqual(url, '/about/')

#     def test_contact_url(self):
#         url = reverse('contact')
#         self.assertEqual(url, '/contact/')

#     def test_cafe_menu_url(self):
#         # Replace 'some-category' with an actual category slug
#         url = reverse('cafe_menu', kwargs={'category_name': 'some-category'})
#         self.assertEqual(url, '/some-category/')

#     def test_save_custom_cart_item_url(self):
#         url = reverse('save_custom_cart_item')
#         self.assertEqual(url, '/save-custom-cart-item/')
#form test
class TestCartAddForm(TestCase):
    def test_valid_form_data(self):
        form = CartAddForm(data={
            'quantity': '5',
            'item_id': '123',
            'action': 'add'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_form_data(self):
        # Test with missing required fields
        form = CartAddForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)  # There should be errors for all fields

class TestSearchForm(TestCase):
    def test_valid_search_data(self):
        form = SearchForm(data={'search': 'test'})
        self.assertTrue(form.is_valid())

    def test_invalid_search_data(self):
        # Test with missing search field
        form = SearchForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)  # There should be an error for the search field\
#admin test
# class CategoryAdminTest(TestCase):
#     def setUp(self):
#         self.category = Category.objects.create(name='Test Category')

#     def test_category_displayed_in_admin(self):
#         site = AdminSite()
#         category_admin = CategoryAdmin(Category, site)
#         self.assertIn(self.category, category_admin.get_queryset(None))

# class ItemAdminTest(TestCase):
#     def setUp(self):
#         self.category = Category.objects.create(name='Test Category')
#         self.item = Item.objects.create(name='Test Item', category=self.category)

#     def test_item_displayed_in_admin(self):
#         site = AdminSite()
#         item_admin = ItemAdmin(Item, site)
#         self.assertIn(self.item, item_admin.get_queryset(None))

# class CafeAdminTest(TestCase):
#     def setUp(self):
#         self.cafe = Cafe.objects.create(name='Test Cafe')

#     def test_cafe_displayed_in_admin(self):
#         site = AdminSite()
#         cafe_admin = CafeAdmin(Cafe, site)
#         self.assertIn(self.cafe, cafe_admin.get_queryset(None))        
#views test
# class TestCafeAppViews(TestCase):
#     def setUp(self):
#         self.category = Category.objects.create(name='Test Category')
#         self.item = Item.objects.create(name='Test Item', category=self.category, price=10.0)
#     def test_about_us_view(self):
#         # Test logic for the about us view
#         response = self.client.get('/about-us/')  # Replace with the actual URL of the about us view
#         self.assertEqual(response.status_code, 200)
#         # Add more assertions as needed to validate the about us view

#     def test_cafe_menu_view(self):
#         # Test logic for the cafe menu view
#         response = self.client.get('/cafe-menu/')  # Replace with the actual URL of the cafe menu view
#         self.assertEqual(response.status_code, 200)
#         # Add more assertions as needed to validate the cafe menu view

#     def test_contact_us_view(self):
#         # Test logic for the contact us view
#         response = self.client.get('/contact-us/')  # Replace with the actual URL of the contact us view
#         self.assertEqual(response.status_code, 200)
#         # Add more assertions as needed to validate the contact us view

#     def test_home_view(self):
#         # Test logic for the home view
#         response = self.client.get('/')  # Replace with the actual URL of the home view
#         self.assertEqual(response.status_code, 200)
#         # Add more assertions as needed to validate the home view

#     def test_save_custom_cart_item_view(self):
#         # Test logic for saving a custom cart item view
#         # Example of posting data to a view
#         data = {
#             'item_id': self.item.id,
#             'quantity': 2,
#         }
#         response = self.client.post('/save-cart-item/', data)  # Replace with the actual URL of the save cart item view
#         self.assertEqual(response.status_code, 200)
#         # Add more assertions as needed to validate the save cart item view