from django.urls import path
from . import views


app_name = "cafe"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutUsView.as_view(), name="about"),
    # path("product_detail/<slug:slug>", product_detail, name="product_detail"),
    path("contact/", views.ContactUsView.as_view(), name="contact"),
    path("<slug:category_name>/", views.CafeMenuView.as_view(), name="cafe_menu"),
    path('save-custom-cart-item/', views.CafeMenuView.as_view(), name='save_custom_cart_item'),
]

