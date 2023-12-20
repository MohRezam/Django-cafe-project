from django.urls import path
from .views import UserLoginView
# from .views import account, bill, staff, manager

# urlpatterns = [
#     path("my_account/", account, name="my_account"),
#     path("bill/", bill, name="bill"),
#     path("staff/", staff, name="staff"),
#     path("manager/", manager, name="manager")
# ]

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="user_login"),
]
