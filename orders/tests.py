from django.test import TestCase
from datetime import date, timedelta
from orders.models import Order, Discount
from .forms import OrderForm, DiscountCodeForm, UserSessionForm, CartAddForm
from .models import Order, Discount
from django.test import TestCase, Client
from django.urls import reverse
from .models import Item
from django.test import TestCase, Client
from django.test import TestCase, Client
from orders.models import Order, Discount  # Import your models here
import json
# from django.contrib.sessions.backends.db import SessionStore
# from orders.custom_session import CustomSession 



class OrderModelTestCase(TestCase):
    def setUp(self):
        self.test_order = Order.objects.create(
            description='Test Order',
            order_date=date.today(),
            table_number=1,
            staff_id='S1',
            order_detail={'item_id': 1, 'quantity': 2},
            order_id='12345',
            customer_name='Test Customer',
            phone_number='1234567890',
            final_price='100.00',
            order_status=True
        )

        self.test_discount = Discount.objects.create(
            code='TESTCODE',
            percentage=20,
            start_date=date.today() - timedelta(days=1),
            end_date=date.today() + timedelta(days=1)
        )
    def test_order_fields(self):
        order = Order.objects.get(description='Test Order')

        self.assertEqual(order.order_date.date(), date.today())
        self.assertEqual(order.table_number, 1)
        self.assertEqual(order.staff_id, 'S1')
        self.assertEqual(order.order_detail, {'item_id': 1, 'quantity': 2})
        self.assertEqual(order.order_id, '12345')
        self.assertEqual(order.customer_name, 'Test Customer')
        self.assertEqual(order.phone_number, '1234567890')
        self.assertEqual(order.final_price, '100.00')
        self.assertTrue(order.order_status)


    def test_discount_methods(self):
        discount = Discount.objects.get(code='TESTCODE')
        self.assertTrue(discount.is_valid())

        # Testing apply_discount method
        amount = 100
        discounted_amount = discount.apply_discount(amount)
        self.assertEqual(discounted_amount, 80)  # 20% discount on 100

    # def test_order_relationships(self):
    #     order = Order.objects.get(description='Test Order')
    #     order.discounts.add(self.test_discount)  # Associate the test discount with the order

    #     discounts = order.discounts.all()
    #     self.assertEqual(discounts.count(), 1)
    #     self.assertEqual(discounts[0].code, 'TESTCODE')

#forms test
class TestOrderForms(TestCase):
    def test_order_form_valid(self):
        form_data = {
            'description': 'Test Order',
            'table_number': 1,
            'customer_name': 'Test Customer',
            'phone_number': '1234567890',
            'discount_code': 'TESTCODE'
        }
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_discount_code_form_valid(self):
        form_data = {
            'code': 'TESTCODE'
        }
        form = DiscountCodeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_session_form_valid(self):
        form_data = {
            'phone_number': '1234567890'
        }
        form = UserSessionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_cart_add_form_valid(self):
        form_data = {
            'quantity': '2',
            'item_id': '1',
            'action': 'add'
        }
        form = CartAddForm(data=form_data)
        self.assertTrue(form.is_valid())

    # def test_order_form_invalid(self):
    #     # Testing invalid data for OrderForm
    #     form_data = {
    #         'description': '',
    #         'table_number': 1,
    #         'customer_name': 'Test Customer',
    #         'phone_number': '1234567890',
    #         'discount_code': 'INVALIDCODE'  # Assuming 'INVALIDCODE' is an invalid code
    #     }
    #     form = OrderForm(data=form_data)
        
    #     self.assertFalse(form.is_valid())  # Check if the form is invalid

    #     # Check for specific errors in individual fields
    #     self.assertIn('description', form.errors)  # Check if 'description' field has an error
    #     self.assertNotIn('discount_code', form.errors)  # Check if 'discount_code' field has no error
    #     # Add similar assertions for other fields that are expected to be invalid or valid

#view test




# class TestCheckoutView(TestCase):
#     def setUp(self):
#         # Create test data if needed (e.g., Discount objects)
#         self.discount = Discount.objects.create(code='TESTCODE', percentage=10)

#     def test_checkout_view_get(self):
#         client = Client()
#         response = client.get(reverse('checkout'))

#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'orders/checkout.html')
#         self.assertContains(response, 'Your checkout content')  # Check for specific content in the HTML
#         # Add more assertions to validate the context, form, etc.

#     def test_checkout_view_post(self):
#         client = Client()
#         data = {
#             # Add form data for the POST request
#         }
#         response = client.post(reverse('checkout'), data)

#         self.assertEqual(response.status_code, 200)
#         # Add more assertions to check the behavior after a POST request to checkout

#     # Add more test cases for CheckoutView as needed


# class TestViewCartView(TestCase):
#     def setUp(self):
#         # Create test data if needed (e.g., Order objects)
#         self.order = Order.objects.create(description='Test Order', table_number=1)

#     def test_view_cart_view_get(self):
#         client = Client()
#         response = client.get(reverse('cart_page'))

#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'orders/cart.html')
#         self.assertContains(response, 'Your cart content')  # Check for specific content in the HTML
#         # Add more assertions to validate the context, form, etc.

#     def test_view_cart_view_post(self):
#         client = Client()
#         data = {
#             # Add form data for the POST request
#         }
#         response = client.post(reverse('cart_page'), data)

#         self.assertEqual(response.status_code, 200)
#         # Add more assertions to check the behavior after a POST request to cart_page

#     def test_delete_cart_item_view(self):
#         client = Client()
#         data = {
#             # Add data for the POST request to delete a cart item
#         }
#         response = client.post(reverse('delete_cart_item'), data)

#         self.assertEqual(response.status_code, 200)
#         # Add assertions to check the behavior after a POST request to delete_cart_item

#     # Add more test cases for ViewCartView as needed

#custom session test


# class TestCustomSessionStore(TestCase):
#     def test_custom_session_store(self):
#         # Create a session store
#         session = SessionStore()
#         session['cart'] = {'item_id': 1, 'quantity': 2}  # Simulating 'cart' data
        
#         # Save the session
#         session.save()

#         # Retrieve or create CustomSession object
#         custom_session = CustomSession.objects.get(session_key=session.session_key)
        
#         # Assertions to check if the CustomSession object has been created correctly
#         self.assertEqual(custom_session.session_key, session.session_key)
#         self.assertEqual(custom_session.custom_data, str(session['cart']))
#         # Add more assertions as needed based on your CustomSession model
        
#         # Clean up: Delete the created CustomSession object
#         custom_session.delete()