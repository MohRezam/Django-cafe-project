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
from .forms import RemoveItemForm
from .forms import EditItemStatusForm
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


class RemoveItemView(View):
    def get(self, request):
        form = RemoveItemForm()
        return render(request, 'remove_item.html', {'form': form})

    def post(self, request):
        form = RemoveItemForm(request.POST)
        if form.is_valid():
            item_id = form.cleaned_data['item_id']
            item = Item.objects.get(id=item_id)
            item.delete()
            messages.success(request, "محصول با موفقیت حذف شد") 
            return redirect('remove_item_url')  # Redirect to the same page to display the form again
        return render(request, 'remove_item.html', {'form': form})


class EditItemStatusView(View):
    def get(self, request):
        form = EditItemStatusForm()
        return render(request, 'edit_item_status.html', {'form': form})

    def post(self, request):
        form = EditItemStatusForm(request.POST)
        if form.is_valid():
            item_id = form.cleaned_data['item_id']
            new_status = form.cleaned_data['new_status']
            item = Item.objects.get(id=item_id)
            item.item_status = new_status
            item.save()
            messages.success(request, "وضعیت محصول با موفقیت ویرایش شد") 
            return redirect('edit_item_status_url')  # Redirect to the same page to display the form again
        return render(request, 'edit_item_status.html', {'form': form})

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
class StaffProfileCategories(LoginRequiredMixin,View):
     def get(sefl,request):
          category = Category.objects.all()
          return render(request,'accounts/categories.html',{'category':category})