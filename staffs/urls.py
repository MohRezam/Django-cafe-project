from django.urls import path
from .views import staffs, manager

urlpatterns = [
    path("staffs/", staffs, name="staffs"),
    path("manager/", manager, name="manager"),
]