from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("<slug:category_name>/", views.CafeMenuView.as_view(), name="cafe_menu"),
    # path("breakfast/", products, name="breakfast"),
    # path("sweets/", products, name="sweets"),
    # path("cafe/", products, name="cafe"),
    # path("maincourse/", products, name="products"),
    # # path("products/<slug:slug>", products, name="products"),
    # # path("menu/", menu, name="menu"),
    # path("product_detail/<slug:slug>", product_detail, name="product_detail"),
    # path("about/", about, name="about"),
]
