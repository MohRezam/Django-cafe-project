from django.urls import path
from . import views
# from .views import add_order, checkout, cart

app_name = "orders"

urlpatterns = [
    path('checkout/', views.CheckoutView.as_view(), name="checkout"),
    path("cart/", views.CartView.as_view(), name="cart_page"),
]


