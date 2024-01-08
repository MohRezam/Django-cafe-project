from django.test import TestCase
from accounts.models import User
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from .models import User
from django.test import TestCase
from .forms import UserLoginForm, UserForm, CategoryForm, ItemForm, UserChangeForm, SortOrdersPhone
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts import views
from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from accounts.admin import UserAdmin
from accounts.forms import UserForm, UserChangeForm
from django.test import TestCase
from django.contrib.auth import get_user_model
#models test
class UserModelTest(TestCase):
    """
    Set up the test environment by creating a User object for testing.
    """
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

#views test
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
#forms test
class TestUserLoginForm(TestCase):
    def test_valid_phone_number(self):
        # Test with valid phone number
        form_data = {
            'phone_number': '12345678901',
            'password': 'some_valid_password',
        }
        form = UserLoginForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_invalid_phone_number(self):
        # Test with invalid phone number (less than 11 digits)
        form_data = {
            'phone_number': '12345',
            'password': 'some_valid_password',
        }
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        
    def test_missing_phone_number(self):
        # Test with missing phone number
        form_data = {
            'password': 'some_valid_password',
        }
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_password(self):
        # Test with valid password
        form_data = {
            'phone_number': '12345678901',
            'password': 'some_valid_password',
        }
        form = UserLoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_password(self):
        # Test with invalid password (empty string)
        form_data = {
            'phone_number': '12345678901',
            'password': '',
        }
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        
    # Test other scenarios (e.g., edge cases, different data combinations) similarly for comprehensive coverage

# Additional tests for other forms (UserForm, CategoryForm, ItemForm, UserChangeForm, SortOrdersPhone) can be written similarly.

#url test

class TestUrls(SimpleTestCase):
    def test_staff_register_url_resolves(self):
        url = reverse('accounts:staff-register')
        self.assertEqual(resolve(url).func.view_class, views.StaffRegisterView)

    def test_staff_profile_url_resolves(self):
        url = reverse('accounts:staff-profile')
        self.assertEqual(resolve(url).func.view_class, views.StffProfileView)

    def test_staff_login_url_resolves(self):
        url = reverse('accounts:staff-login')
        self.assertEqual(resolve(url).func.view_class, views.StaffLoginView)

    def test_staff_logout_url_resolves(self):
        url = reverse('accounts:staff-logout')
        self.assertEqual(resolve(url).func.view_class, views.StffLogoutView)

    def test_staff_profile_info_url_resolves(self):
        url = reverse('accounts:staff-profile-info', args=[1])  # Replace 1 with an actual staff user ID for testing
        self.assertEqual(resolve(url).func.view_class, views.StaffProfileInfoView)

    def test_staff_personal_info_url_resolves(self):
        url = reverse('accounts:staff-personal-info')
        self.assertEqual(resolve(url).func.view_class, views.StaffProfilePersonalView)

    # Continue adding similar test methods for the rest of your URLs
    
    def test_staff_reports_insights_url_resolves(self):
        url = reverse('accounts:staff-reports-insights')
        self.assertEqual(resolve(url).func.view_class, views.StaffReportsInsightsView)

    def test_staff_orders_url_resolves(self):
        url = reverse('accounts:staff-orders')
        self.assertEqual(resolve(url).func.view_class, views.StaffProfileOrdersView)
    def test_staff_profile_categories_url_resolves(self):
        url = reverse('accounts:staff-categories')
        self.assertEqual(resolve(url).func.view_class, views.StaffProfileCategoriesView)

    def test_staff_category_delete_url_resolves(self):
        url = reverse('accounts:staff-category-delete', args=[1])  # Replace 1 with an actual category ID for testing
        self.assertEqual(resolve(url).func.view_class, views.StaffCategoryDeleteView)

    def test_staff_category_update_url_resolves(self):
        url = reverse('accounts:staff-category-update', args=[1])  # Replace 1 with an actual category ID for testing
        self.assertEqual(resolve(url).func.view_class, views.StaffCategoryUpdateView)

    def test_staff_add_category_url_resolves(self):
        url = reverse('accounts:staff-add-category')
        self.assertEqual(resolve(url).func.view_class, views.StaffAddCategoryView)

    def test_staff_profile_items_url_resolves(self):
        url = reverse('accounts:staff-items')
        self.assertEqual(resolve(url).func.view_class, views.StaffProfileItemsView)

    def test_staff_profile_delete_item_url_resolves(self):
        url = reverse('accounts:staff-delete-item', args=[1])  # Replace 1 with an actual item ID for testing
        self.assertEqual(resolve(url).func.view_class, views.StaffProfileDeleteItemView)

    def test_staff_profile_update_item_url_resolves(self):
        url = reverse('accounts:staff-update-item', args=[1])  # Replace 1 with an actual item ID for testing
        self.assertEqual(resolve(url).func.view_class, views.StaffProfileUpdateItemView)

    def test_staff_profile_add_item_url_resolves(self):
        url = reverse('accounts:staff-add-item')
        self.assertEqual(resolve(url).func.view_class, views.StaffProfileAddItemView)

    def test_staff_order_uncomplete_url_resolves(self):
        url = reverse('accounts:staff-orders-uncomplete')
        self.assertEqual(resolve(url).func.view_class, views.StaffProfileOrderUncompleteView)

    def test_staff_order_complete_url_resolves(self):
        url = reverse('accounts:staff-orders-complete')
        self.assertEqual(resolve(url).func.view_class, views.StaffProfileOrdercompleteView)

    def test_staff_order_detail_url_resolves(self):
        url = reverse('accounts:staff-order-detail', args=[1])  # Replace 1 with an actual order ID for testing
        self.assertEqual(resolve(url).func.view_class, views.StaffProfileOrderDetailView)
    def test_staff_orders_url_resolves(self):
        url = reverse('accounts:staff-orders')
        self.assertEqual(resolve(url).func.view_class, views.StaffProfileOrdersView)

    def test_staff_reports_insights_url_resolves(self):
        url = reverse('accounts:staff-reports-insights')
        self.assertEqual(resolve(url).func.view_class, views.StaffReportsInsightsView)
#admin test
        
User = get_user_model()

class TestUserAdmin(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = UserAdmin(User, self.site)

    def test_admin_instantiation(self):
        self.assertIsInstance(self.admin, UserAdmin)

    def test_list_display(self):
        self.assertEqual(self.admin.list_display, ('email', 'phone_number', 'is_admin'))

    def test_list_filter(self):
        self.assertEqual(self.admin.list_filter, ('is_admin',))

    def test_fieldsets(self):
        fieldsets = self.admin.fieldsets
        self.assertEqual(len(fieldsets), 2)  # Ensure there are two fieldsets defined

        # Test the content of fieldsets
        self.assertEqual(fieldsets[0][0], None)  # First fieldset should have a title 'None'
        self.assertListEqual(
            list(fieldsets[0][1]['fields']),
            ['email', 'phone_number', 'full_name', 'password', 'address', 'national_id']
        )  # Ensure fields are included correctly

        self.assertEqual(fieldsets[1][0], 'Permissions')  # Second fieldset should have a title 'Permissions'
        self.assertListEqual(
            list(fieldsets[1][1]['fields']),
            ['is_active', 'is_admin', 'last_login']
        )  # Ensure permissions fields are included correctly
#manager tests
        
User = get_user_model()

class TestUserManager(TestCase):
    def test_create_user(self):
        # Ensure a valid 11-digit phone number is used for testing
        valid_phone_number = '12345678901'  
        user = User.objects.create_user(
            phone_number=valid_phone_number,
            email='test@example.com',
            full_name='Test User',
            password='testpassword'
        )
        self.assertIsNotNone(user)
        self.assertFalse(user.is_admin)
        self.assertEqual(user.phone_number, valid_phone_number)
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.full_name, 'Test User')
        self.assertEqual(user.address, None)
        self.assertEqual(user.national_id, None)
        self.assertTrue(user.check_password('testpassword'))
    def test_create_superuser(self):
        superuser = User.objects.create_superuser(
            phone_number='12345678990',
            email='admin@example.com',
            full_name='Admin User',
            password='adminpassword'
        )
        self.assertIsNotNone(superuser)
        self.assertTrue(superuser.is_admin)
        self.assertEqual(superuser.phone_number, '12345678990')
        self.assertEqual(superuser.email, 'admin@example.com')
        self.assertEqual(superuser.full_name, 'Admin User')
        self.assertEqual(superuser.address, None)  # Assuming 'address' and 'national_id' default to None
        self.assertEqual(superuser.national_id, None)
        self.assertTrue(superuser.check_password('adminpassword'))

    # Add more test methods to verify add_fieldsets, search_fields, ordering, filter_horizontal, etc.
       