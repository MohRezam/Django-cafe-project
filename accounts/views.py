from django.shortcuts import render, redirect
from .forms import UserLoginForm
from django.views import View
from cafe.models import Item,Category
from accounts.models import User
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

class AddCategoryView(View):
    def get(self,request):
        form = CategoryForm()
        return render(request, 'profile-add-category.html', {'form': form})

    def post(self,request):
            form = CategoryForm(request.POST)
            if form.is_valid():
                category = Category(
                    name=form.cleaned_data['name']
                )
                category.save()
                messages.success(request, 'دسته بندی با موفقیت اضافه شد.')
                return render(request, 'profile-add-category.html', {'form': CategoryForm()})


class AddItemView(View):
    def get(self,request):
        form = AddItemForm()
        return render(request, 'profile-item-add.html', {'form': form})

    def post(self,request):
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
            return redirect('profile-items.html')

# class UserEditView(UpdateView):
#     model = User
#     form_class = UserEditForm
#     template_name = 'profile-additional-info.html'
#     success_url = reverse_lazy('profile-personal-info')  # Redirect to the user profile or another page
#     def get_object(self, queryset=None):
#         user_id = self.kwargs.get('user_id')
#         return User.objects.filter(id=user_id).first()  # Retrieve the user from the database
    
#     def form_valid(self, form):
#         user_id = self.kwargs.get('user_id')
#         user = self.get_object()
#         if user:
#             # Update user information with the form data
#             user.full_name = form.cleaned_data['full_name']
#             user.phone_number = form.cleaned_data['phone_number']
#             user.email = form.cleaned_data['email']
#             user.save()
#             messages.success(self.request, 'اطلاعات کاربر با موفقیت ویرایش شد.')  # Success message
#         else:
#             messages.error(self.request, 'کاربر مورد نظر یافت نشد.')  # User not found message
#             return redirect('user_list')  # Redirect to a user list or another appropriate page
#         return super().form_valid(form)

