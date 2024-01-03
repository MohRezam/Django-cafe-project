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
    path('profile-categories/',views.StaffProfileCategoriesView.as_view(),name="staff-categories"),
    path('profile-category-delete/<int:id_category>/',views.StaffCategoryDeleteView.as_view(),name="staff-category-delete"),
    path('profile-category-update/<int:id_category>/',views.StaffCategoryUpdateView.as_view(),name="staff-category-update"),
    path('profile-add-category/',views.StaffAddCategoryView.as_view(),name="staff-add-category"),
    path('profile-items/',views.StaffProfileItemsView.as_view(),name="staff-items"),
    path('profile-item-delete/<int:id_item>/',views.StaffProfileDeleteItemView.as_view(),name="staff-delete-item"),
    path('profile-item-update/<int:id_item>/',views.StaffProfileUpdateView.as_view(),name="staff-update-item")
]
