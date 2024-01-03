from django.shortcuts import render, redirect , get_object_or_404
from .forms import UserLoginForm,UserForm,UserChangeForm,CategoryForm,ItemForm
from django.views import View
from cafe.models import Item,Category
from accounts.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login,authenticate,logout
from django.views.generic import TemplateView
from django.db.models import Count, Sum
from django.utils import timezone
from orders.models import OrderItem, Order
import csv
from django.http import HttpResponse
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
class StaffProfileCategoriesView(LoginRequiredMixin,View):
     def get(self,request):
          category = Category.objects.all()
          return render(request,'accounts/categories.html',{'category':category})
class StaffCategoryDeleteView(LoginRequiredMixin,View):
     def get(self,request,id_category):
          category = get_object_or_404(Category, pk=id_category)
          category.delete()
          messages.success(request,"دسته بندی با موفقیت حذف شد","success")
          return redirect("accounts:staff-categories")
class StaffCategoryUpdateView(LoginRequiredMixin, View):
    form_class = CategoryForm
    template_name = "accounts/profile-update-category.html"
    
    def get(self, request, id_category):
        category = get_object_or_404(Category, id=id_category)
        form = self.form_class(instance=category)
        return render(request, self.template_name, {'form': form})
        
    def post(self, request, id_category):
        category = get_object_or_404(Category, id=id_category)
        form = self.form_class(request.POST, instance=category)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'آپدیت اطلاعات شخصی با موفقیت انجام شد', 'success')
            return redirect('accounts:staff-categories')
        
        return render(request, self.template_name, {'form': form})   
class StaffAddCategoryView(LoginRequiredMixin, View):
    form_class = CategoryForm
    template_name = "accounts/profile-add-category.html"
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        
        if form.is_valid():
            cd = form.cleaned_data
            category = Category.objects.create()
            category.category_name = cd['category_name']
            category.image = cd['image']
            category.created_at = cd['created_at']
            category.save()
            messages.success(request, 'دسته بندی جدید با موفقیت ایجاد شد', 'success')
            return redirect('accounts:staff-categories')
        
        return render(request, self.template_name, {'form': form})
class StaffProfileItemsView(LoginRequiredMixin,View):
    def get(self,request):
        items = Item.objects.all()
        return render(request,'accounts/items.html',{'items':items})
class StaffProfileDeleteItemView(LoginRequiredMixin,View):
     def get(self,request,id_item):
          item = get_object_or_404(Item, pk=id_item)
          item.delete()
          messages.success(request,"محصول با موفقیت حذف شد","success")
          return redirect("accounts:staff-items")
class StaffProfileUpdateView(LoginRequiredMixin,View):
     form_class = ItemForm
     template_name = "accounts/profile-add-item.html"
     def get(self,request,id_item) :
        item = get_object_or_404(Item, id=id_item)
        form = self.form_class(instance=item)
        return render(request, self.template_name, {'form': form})
     
     def post(self,request,id_item):
        item = get_object_or_404(Item, id=id_item)
        form = self.form_class(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'آپدیت محصول با موفقیت انجام شد', 'success')
            return redirect('accounts:staff-items')
        else:
            form = self.form_class(instance=item)
            return render(request, self.template_name, {'form': form})  
class StatisticsView(TemplateView):
    template_name = 'statistics.html' # Here, you can enter the template name you want to show the statestics

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Most ordered items and their quantities
        context['most_ordered_items'] = OrderItem.objects.values('item').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:20]

        # Most reserved tables
        context['most_reserved_tables'] = Order.objects.values('table_number').annotate(total_reservations=Count('id')).order_by('-total_reservations')[:20]

        # Peak business hours
        context['peak_hours'] = Order.objects.filter(order_date__date=timezone.now().date()).values('order_date__hour').annotate(total_orders=Count('id')).order_by('-total_orders')[:20]

        # Total sales
        context['total_sales'] = OrderItem.objects.aggregate(total_sales=Sum('item__price'))

        return context
    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="statistics.csv"'

            writer = csv.writer(response)
            writer.writerow(['Item Name', 'Total Quantity'])
            for item in self.get_context_data()['most_ordered_items']:
                writer.writerow([item['item__name'], item['total_quantity']])

            writer.writerow([]) # Add an empty row for separation

            writer.writerow(['Table Number', 'Total Reservations'])
            for table in self.get_context_data()['most_reserved_tables']:
                writer.writerow([table['table_number'], table['total_reservations']])

            writer.writerow([])  

            writer.writerow(['Order Hour', 'Total Orders'])
            for hour in self.get_context_data()['peak_hours']:
                writer.writerow([hour['order_date__hour'], hour['total_orders']])

            writer.writerow([])  

            writer.writerow(['Total Sales'])
            writer.writerow([self.get_context_data()['total_sales']['total_sales']])

            return response
        else:
            return HttpResponse("You are not authorized to download the statistics.", status=403)