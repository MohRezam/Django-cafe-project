from django.urls import path
from . import views
from .views import ViewCartView

app_name = "orders"

urlpatterns = [
    path('checkout/', views.CheckoutView.as_view(), name="checkout"),
    path("cart/", ViewCartView.as_view(), name="cart_page"),
    # path('edit_cart/', EditCookieView.as_view(), name='editcart'),
    path('delete-cart-item/', ViewCartView.as_view(), name='delete_cart_item'),


]


