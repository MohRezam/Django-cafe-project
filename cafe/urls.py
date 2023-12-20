from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("cart/", views.CartView.as_view(), name="cart_page"),
    path("<slug:category_name>/", views.CafeMenuView.as_view(), name="cafe_menu"),
    # path("product_detail/<slug:slug>", product_detail, name="product_detail"),
    # path("about/", about, name="about"),
]
