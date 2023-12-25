from django.shortcuts import render, redirect
from .forms import UserLoginForm
from django.views import View
from cafe.models import Item
from cafe.models import Category
from django.contrib import messages
from .forms import CategoryForm
from .authenticate import PhoneBackend
from django.contrib.auth import login
from .forms import AddItemForm
# Create your views here.

    
class StaffLoginView(View):
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
            category = Category(
                name=form.cleaned_data['name']
            )
            category.save()
            messages.success(request, 'دسته بندی با موفقیت اضافه شد.')  # Success message
            return render(request, 'profile-add-category.html', {'form': CategoryForm()})
    else:
        form = CategoryForm()
    return render(request, 'profile-add-category.html', {'form': form})

def add_item_view(request):
    if request.method == 'POST':
        #it allows the form to upload files (e.g., images, documents)
        # In such cases, request.FILES stores the uploaded files.
        form = AddItemForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the form data (save to database, etc.)
            # Example: Save the form data to a model
            item = Item(
                name=form.cleaned_data['name'],
                fixed_number=form.cleaned_data['fixed_number'],
                category=form.cleaned_data['category'],
                description=form.cleaned_data['description'],
                form_file=form.cleaned_data['form_file']
            )
            item.save()
            messages.success(request, 'آیتم با موفقیت اضافه شد.')
            return redirect('profile-items.html')  # Change 'success_page' to your success URL name
    else:
        form = AddItemForm()
    
    return render(request, 'profile-item-add.html', {'form': form})

class StaffProfilesView(View):
    def get(self,request):
        pass
    def post(self,request):
        pass

