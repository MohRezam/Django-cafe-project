from django.urls import path
from . import views


app_name = "accounts"

urlpatterns = [
    path("login/", views.StaffLoginView.as_view(), name="staff-login"),
    # path("profile/<str:phone_number>",views.StaffProfilesView.as_view(),name="staff-profile"),
    # path("categories/<str:phone_number>",views.StaffCategoriesView.as_view(),name="staff-categories"),
    # path("add-category/<str:phone_number>",views.StaffAddCategoryView.as_view(),name="staff-add-category"),
    # path("items/<str:phone_number>",views.StaffItesmView.as_view(),name="staff-items"),
    # path("add-item/<str:phone_number>",views.StaffAddItemView.as_view(),name="staff-add-item"),
    # path("update-profile/<str:phone_number>",views.StaffUpdateProfileView.as_view(),name="update-profile")
]
