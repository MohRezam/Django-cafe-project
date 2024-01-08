from .models import User
from django.contrib.auth.backends import BaseBackend
class PhoneBackend(BaseBackend):
    """
        Authenticates a user based on their phone number and password.

        Args:
            request (HttpRequest): The current request object.
            username (str): The phone number of the user.
            password (str): The password provided by the user.

        Returns:
            User: The authenticated user object if successful, None otherwise.
    """
    def authenticate(request, username=None, password=None):
        try:
            user = User.objects.get(phone_number=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None    
    
    
    def get_user(self, user_id):
        """
        Retrieves a user object based on the provided user ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            User: The user object if found, None otherwise.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        