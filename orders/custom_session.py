from django.contrib.sessions.backends.db import SessionStore as DbSessionStore
from .models import CustomSession

class CustomSessionStore(DbSessionStore):
    def save(self, must_create=False):
        super().save(must_create)

        # If 'cart' exists in the session data, save it in the CustomSession model
        if 'cart' in self._session:
            custom_session, created = CustomSession.objects.get_or_create(session_key=self.session_key)
            custom_session.custom_data = str(self._session['cart'])  
            custom_session.save()