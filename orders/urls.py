from django.urls import path
from . import views
# from .views import add_order, checkout, cart

urlpatterns = [
    path('checkout/', views.CheckoutView.as_view(), name="checkout"),
]


