from django.urls import path
from .views import account, bill, staff, manager

urlpatterns = [
    path("my_account/", account, name="my_account"),
    path("bill/", bill, name="bill"),
    path("staff/", staff, name="staff"),
    path("manager/", manager, name="manager")
]