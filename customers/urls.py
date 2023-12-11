from django.urls import path
from .views import account, bill

urlpatterns = [
    path("my_account/", account, name="my_account"),
    path("bill/", bill, name="bill"),
]