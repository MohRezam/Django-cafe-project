from django.test import TestCase
from accounts.models import User
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from .models import User

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


class AccountsViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email='test@example.com', phone_number='12345678901', full_name='Test User', password='testpassword')

    def test_staff_login_view(self):
        response = self.client.get(reverse('accounts:staff-login'))
        self.assertEqual(response.status_code, 200)  # Check if the login page loads successfully

        form_data = {
            'phone_number': '12345678901',  # Replace with your test phone number
            'password': 'testpassword',  # Replace with your test password
        }
        response = self.client.post(reverse('accounts:staff-login'), form_data, follow=True)
        
        # Check if the login is successful and redirects to the profile page
        self.assertEqual(response.status_code, 200)  # Check if the redirection happened successfully
        self.assertTemplateUsed(response, 'accounts/profile.html')  # Check if the correct template is used for the profile page

    def test_staff_profile_view(self):
        self.client.login(email='test@example.com', password='testpassword')
        response = self.client.get(reverse('accounts:staff-profile'))
        self.assertEqual(response.status_code, 302)  # Check if the redirection happens after successful login
    def test_staff_logout_view(self):
        self.client.login(email='test@example.com', password='testpassword')
        response = self.client.get(reverse('accounts:staff-logout'))
        self.assertEqual(response.status_code, 302)  # Check if the redirection after logout is successful
