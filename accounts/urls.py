from django.urls import path
from . import views


app_name = "accounts"

urlpatterns = [
    path('register/',views.StaffRegisterView.as_view(),name="staff-register"),
    path('profile/',views.StffProfileView.as_view(),name="staff-profile"),
    path('login/',views.StaffLoginView.as_view(),name="staff-login"),
    path('Logout/',views.StffLogoutView.as_view(),name="staff-logout")
]
