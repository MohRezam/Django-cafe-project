from django.shortcuts import render, redirect
from .forms import UserLoginForm,UserForm,UserChangeForm
from django.views import View
from cafe.models import Item,Category
from accounts.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CategoryForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login,authenticate,logout
from .forms import AddItemForm
# Create your views here.

class StaffRegisterView(View):
    form_class = UserForm  
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(email=cd['email'],phone_number=cd['phone_number'],full_name = cd['full_name'] , password=cd['password'])  
            user.address = cd['address']
            user.national_id = cd['national_id']
            user.is_active = cd['is_active']
            user.is_admin = cd['is_admin']
            user.save()  
            messages.success(request, 'ثبت نام شما با موفقیت انجام شد', 'success')
            return redirect('accounts:staff-profile')
        return render(request, self.template_name, {'form': form})


    
class StaffLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['phone_number'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you logged in successfully', 'success')
                return redirect('accounts:staff-profile')
            messages.error(request, 'این شماره تلفن یا رمز عبور درست نمی باشد', 'warning')
        return render(request, self.template_name, {'form': form})
    
class StffLogoutView(LoginRequiredMixin, View):
	def get(self, request):
		logout(request)
		messages.success(request, 'خروج موفقیت آمیز انجام شد', 'success')
		return redirect('accounts:staff-login')


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
        
class StffProfileView(LoginRequiredMixin,View):
     def get(slef,request):
          return render(request,'accounts/profile.html')
     

class StaffProfileInfoView(LoginRequiredMixin, View):
    form_class = UserChangeForm
    template_name = "accounts/profile-info.html"

    def get(self, request, staff_user_id):
        user = User.objects.get(id=staff_user_id)
        form = self.form_class(instance=user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, staff_user_id):
        user = User.objects.get(id=staff_user_id)
        form = self.form_class(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'آپدیت اطلاعات شخصی با موفقیت انجام شد', 'success')
            return redirect('accounts:staff-profile')
        else:
            form = self.form_class(instance=user)
            return render(request, self.template_name, {'form': form})
class StaffProfilePersonalView(LoginRequiredMixin, View):
     def get(self,request):
          return render(request,'accounts/profile-personal-info.html')
