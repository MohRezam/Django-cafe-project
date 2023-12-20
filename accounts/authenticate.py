from .models import User


class PhoneBackend:
    def authenticate(request, username=None, password=None):
        try:
            user = User.objects.get(phone_number=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None    
    
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None