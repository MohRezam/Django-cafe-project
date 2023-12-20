from django.shortcuts import render, redirect
from .forms import UserLoginForm
from django.views import View
from .authenticate import PhoneBackend
from django.contrib.auth import login
# Create your views here.

# def account(request):
#     if request.method == "GET":
#         return render(request, "", context={})
    
    
# def bill(request):
#     if request.method == "GET":
#         return render(request, "", context={})
    
# def staff(request):
#     if request.method == "GET":
#         return render(request, "", context={})
    
# def manager(request):
#     if request.method == "GET":
#         return render(request, "", context={})
    
    
class UserLoginView(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, "accounts/login.html", {"form":form})
            
    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = PhoneBackend.authenticate(request, username=cd["phone_number"], password=cd["password"])
            if user is not None:
                login(request, user)
                return render(request, "accounts/staff")
        return render(request, "accounts/login.html", {"form":form})
