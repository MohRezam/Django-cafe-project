from django.urls import path
from . import views


app_name = "accounts"

urlpatterns = [
    path("login/", views.StaffLoginView.as_view(), name="staff-login"),
    path("profile/<str:username>/",views.StaffProfilesView.as_view(),name="staff-profile")
]
