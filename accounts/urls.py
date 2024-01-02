from django.urls import path
from . import views


app_name = "accounts"

urlpatterns = [
    path('register/',views.StaffRegisterView.as_view(),name="staff-register"),
    path('profile/',views.StffProfileView.as_view(),name="staff-profile"),
    path('login/',views.StaffLoginView.as_view(),name="staff-login"),
    path('Logout/',views.StffLogoutView.as_view(),name="staff-logout"),
    path('profile-info/<int:staff_user_id>/',views.StaffProfileInfoView.as_view(),name="staff-profile-info"),
    path('profile-personal-info/',views.StaffProfilePersonalView.as_view(),name="staff-personal-info"),
    path('profile-categories/',views.StaffProfileCategories.as_view(),name="staff-categories")
]
