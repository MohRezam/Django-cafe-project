from django.apps import AppConfig


class OrdersConfig(AppConfig):
    """
    AppConfig subclass for the 'orders' app.
    """
    # Use the 'BigAutoField' as the default auto field for this app
    default_auto_field = 'django.db.models.BigAutoField'
    # Set the name of the app to 'orders'
    name = 'orders'
