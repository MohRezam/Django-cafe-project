from django.urls import path
from . import views


app_name = "cafe"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    # path("product_detail/<slug:slug>", product_detail, name="product_detail"),
    path("<slug:category_name>/", views.CafeMenuView.as_view(), name="cafe_menu"),
]
