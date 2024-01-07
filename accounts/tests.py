from django.test import TestCase
from accounts.models import User
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

class UserModelTest(TestCase):
    def setUp(self):
        # Create a User object for testing
        self.user = User.objects.create(
            email='test@example.com',
            phone_number='12345678901',
            full_name='Test User'
        )


    def test_email_field(self):
        # Test unique email constraint by catching IntegrityError
        with self.assertRaises(IntegrityError):
            User.objects.create(email='test@example.com', phone_number='11111111111', full_name='Another User')

    def test_phone_number_field(self):
        # Test unique phone number constraint by catching IntegrityError
        with self.assertRaises(IntegrityError):
            User.objects.create(email='test2@example.com', phone_number='12345678901', full_name='Yet Another User')
    def test_convert_to_english_numbers_method(self):
        user = self.user
        persian_number = '۱۲۳۴۵۶۷۸۹۰'
        english_number = '1234567890'
        self.assertEqual(user.convert_to_english_numbers(persian_number), english_number)

    def test_clean_email_method(self):
        user = self.user
        cleaned_email = user.clean_email('test@example.com')
        self.assertEqual(cleaned_email, 'test@example.com')
    def test_clean_phone_number_method(self):
        with self.assertRaises(ValueError) as context:
            cleaned_phone_number = self.user.clean_phone_number('۱۲۳۴۵۶۷۸۹')
        self.assertEqual(str(context.exception), 'Phone number should be 11 digits long.')