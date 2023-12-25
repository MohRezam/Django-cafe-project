from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from .forms import UserLoginForm
from django.views import View
from .authenticate import PhoneBackend
from django.contrib.auth import login
import datetime
from  .models import User
# Create your views here.

    
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
                login(request, user, backend="django.contrib.auth.backends.ModelBackend")
                return render(request, "accounts/staff.html")
        return render(request, "accounts/login.html", {"form":form})



#