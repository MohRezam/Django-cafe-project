from django.urls import path
from .views import home, product_detail, products, about

urlpatterns = [
    path("", home, name="home"),
    path("breakfast/", products, name="breakfast"),
    path("sweets/", products, name="sweets"),
    path("cafe/", products, name="cafe"),
    path("maincourse/", products, name="products"),
    # path("products/<slug:slug>", products, name="products"),
    # path("menu/", menu, name="menu"),
    path("product_detail/<slug:slug>", product_detail, name="product_detail"),
    path("about/", about, name="about"),
]
