from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Configuration class for the 'accounts' app.
    
    This class defines the configuration options for the 'accounts' app in a Django project.
    It sets the default auto field and specifies the name of the app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
