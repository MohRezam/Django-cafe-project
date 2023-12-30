from django.urls import path
from . import views
from .views import ViewCartView

app_name = "orders"

urlpatterns = [
    path('checkout/', views.CheckoutView.as_view(), name="checkout"),
    path("cart/", ViewCartView.as_view(), name="cart_page"),
]


