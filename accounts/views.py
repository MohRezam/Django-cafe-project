from django.shortcuts import render, redirect
from .forms import UserLoginForm
from django.views import View
from django.contrib import messages
from .forms import CategoryForm
from .authenticate import PhoneBackend
from django.contrib.auth import login
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
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            messages.success(request, 'دسته بندی با موفقیت اضافه شد.')  # Success message
            return render(request, 'profile-add-category.html', {'form': CategoryForm()})
    else:
        form = CategoryForm()
    return render(request, 'profile-add-category.html', {'form': form})