from django.test import TestCase
from datetime import date, timedelta
from orders.models import Order, Discount

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
