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
from orders.models import Order
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
    model = Order
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
         # Most ordered items and their quantities
        context['most_ordered_items'] = Order.objects.values('order_detail__item').annotate(total_quantity=Sum('order_detail__quantity')).order_by('-total_quantity')[:20]

        # Most reserved tables
        context['most_reserved_tables'] = Order.objects.values('table_number').annotate(total_reservations=Count('id')).order_by('-total_reservations')[:20]

       # Peak business hours
        context['peak_hours'] = Order.objects.filter(order_date__date=timezone.now().date()).values('order_date__hour').annotate(total_orders=Count('id')).order_by('-total_orders')[:20]

        # Total sales
        context['total_sales'] = Order.objects.aggregate(total_sales=Sum('order_detail__item__price'))
        
        # Monthly sales
        context['monthly_sales'] = Order.objects.filter(order_date__month=timezone.now().month).aggregate(total_sales=Sum('order_detail__item__price'))

        # Yearly sales
        context['yearly_sales'] = Order.objects.filter(order_date__year=timezone.now().year).aggregate(total_sales=Sum('order_detail__item__price'))

        # Top-selling items (filtered by date)
        context['top_selling_items'] = Order.objects.filter(order_date__date=timezone.now().date()).values('order_detail__item').annotate(total_quantity=Sum('order_detail__quantity')).order_by('-total_quantity')[:20]

        # Sales by category
        context['sales_by_category'] = Order.objects.values('order_detail__item__category').annotate(total_sales=Sum('order_detail__item__price')).order_by('-total_sales')

        # Sales based on customer (phone)
        context['sales_by_customer'] = Order.objects.values('phone_number').annotate(total_sales=Sum('order_detail__item__price')).order_by('-total_sales')

        # Sales based on time of day
        context['sales_by_time_of_day'] = Order.objects.values('order_date__hour').annotate(total_sales=Sum('order_detail__item__price')).order_by('order_date__hour')

        # Order status report (daily)
        context['order_status_report'] = Order.objects.filter(order_date__date=timezone.now().date()).values('status').annotate(total_orders=Count('id')).order_by('status')

        # Daily sales
        context['daily_sales'] = Order.objects.filter(order_date__date=timezone.now().date()).aggregate(total_sales=Sum('order_detail__item__price'))

        # Sales by employee report
        context['sales_by_employee_report'] = Order.objects.values('staff_id__username').annotate(total_sales=Sum('order_detail__item__price')).order_by('-total_sales')

        # Customer order history report
        context['customer_order_history_report'] = Order.objects.filter(phone_number=self.request.user.phone_number).order_by('-order_date')

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

            writer.writerow([])

            writer.writerow(['Monthly Sales'])
            writer.writerow(['Month', 'Total Sales'])
            for month in monthly_sales:
                writer.writerow([calendar.month_name[month['month']], month['total_sales']])

            writer.writerow([])  

            writer.writerow(['Yearly Sales'])
            writer.writerow(['Year', 'Total Sales'])
            for year in yearly_sales:
                writer.writerow([year['year'], year['total_sales']])

            writer.writerow([])  

            writer.writerow(['Top Selling Items'])
            writer.writerow(['Item Name', 'Total Quantity'])
            for item in top_selling_items:
                writer.writerow([item['item__name'], item['total_quantity']])

            writer.writerow([]) 

            writer.writerow(['Sales by Category'])
            writer.writerow(['Category', 'Total Sales'])
            for category in sales_by_category:
                writer.writerow([category['item__category__name'], category['total_sales']])

            writer.writerow([]) 

            writer.writerow(['Sales by Customer'])
            writer.writerow(['Customer', 'Total Sales'])
            for customer in sales_by_customer:
                writer.writerow([customer['customer__name'], customer['total_sales']])

            writer.writerow([])  

            writer.writerow(['Sales by Time of Day'])
            writer.writerow(['Hour', 'Total Sales'])
            for hour in sales_by_time_of_day:
                writer.writerow([hour['hour'], hour['total_sales']])

            writer.writerow([])  

            writer.writerow(['Order Status Report'])
            writer.writerow(['Status', 'Total Orders'])
            for status in order_status_report:
                writer.writerow([status['status'], status['total_orders']])

            writer.writerow([])  

            writer.writerow(['Daily Sales'])
            writer.writerow(['Date', 'Total Sales'])
            for day in daily_sales:
                writer.writerow([day['date'], day['total_sales']])

            return response
        else:
            return HttpResponse("You are not authorized to download the statistics.", status=403)