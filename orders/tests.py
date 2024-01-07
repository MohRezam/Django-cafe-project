from django.test import TestCase
from datetime import date, timedelta
from orders.models import Order, Discount
from .forms import OrderForm, DiscountCodeForm, UserSessionForm, CartAddForm
from .models import Order, Discount

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