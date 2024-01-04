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
from django.views.generic import TemplateView
from django.db.models import Count, Sum
from django.utils import timezone
from orders.models import Order
import csv
from django.http import HttpResponse
import calendar
from datetime import date
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

class StatisticsView(TemplateView):
    template_name = 'statistics.html'
    model = Order
    
    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="statistics.csv"'
            context = self.get_context_data(**kwargs)

            # Most ordered items and their quantities
            context['most_ordered_items'] = Order.objects.values('order_detail__item__name').annotate(total_quantity=Sum('order_detail__quantity')).order_by('-total_quantity')[:20]

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
            context['top_selling_items'] = Order.objects.filter(order_date__date=timezone.now().date()).values('order_detail__item__name').annotate(total_quantity=Sum('order_detail__quantity')).order_by('-total_quantity')[:20]

            # Sales by category
            context['sales_by_category'] = Order.objects.values('order_detail__item__category').annotate(total_sales=Sum('order_detail__item__price')).order_by('-total_sales')

            # Sales based on customer (phone)
            context['sales_by_customer'] = Order.objects.values('phone_number').annotate(total_sales=Sum('order_detail__item__price')).order_by('-total_sales')

            # Sales based on time... (add your logic) # Sales based on time of day
            context['sales_by_time_of_day'] = Order.objects.values('order_date__hour').annotate(total_sales=Sum('order_detail__item__price')).order_by('order_date__hour')

            # Order status report (daily)
            context['order_status_report'] = Order.objects.filter(order_date__date=timezone.now().date()).values('status').annotate(total_orders=Count('id')).order_by('status')

            # Daily sales
            context['daily_sales'] = Order.objects.filter(order_date__date=timezone.now().date()).aggregate(total_sales=Sum('order_detail__item__price'))

            # Sales by employee report
            context['sales_by_employee_report'] = Order.objects.values('staff_id__username').annotate(total_sales=Sum('order_detail__item__price')).order_by('-total_sales')

            # Customer order history report
            context['customer_order_history_report'] = Order.objects.filter(phone_number=self.request.user.phone_number).order_by('-order_date')

            self.write_to_csv(response, context)

            return response
        else:
            return HttpResponse("You are not authorized to download the statistics.", status=403)

    def write_to_csv(self, response, context):
        writer = csv.writer(response)

        writer.writerow(['Item Name', 'Total Quantity'])
        for item in context['most_ordered_items']:
            writer.writerow([item['order_detail__item__name'], item['total_quantity']])

        writer.writerow([])  # Add an empty row for separation
        writer.writerow(['Table Number', 'Total Reservations'])
        for table in context['most_reserved_tables']:
            writer.writerow([table['table_number'], table['total_reservations']])
        
        # Peak business hours
        writer.writerow([])  
        writer.writerow(['Order Hour', 'Total Orders'])
        for hour in context['peak_hours']:
            writer.writerow([hour['order_date__hour'], hour['total_orders']])

        # Total_sales
        writer.writerow([])  
        writer.writerow(['Total Sales'])
        writer.writerow([context['total_sales']['total_sales']])

        # Monthly_sales
        writer.writerow([])
        writer.writerow(['Monthly Sales'])
        writer.writerow(['Month', 'Total Sales'])
        for month in context['monthly_sales']:
            writer.writerow([calendar.month_name[month['month']], month['total_sales']])

        # Yearly_sales
        writer.writerow([])  
        writer.writerow(['Yearly Sales'])
        writer.writerow(['Year', 'Total Sales'])
        for year in context['yearly_sales']:
            writer.writerow([year['year'], year['total_sales']])

        # top_selling_items
        writer.writerow([])  
        writer.writerow(['Top Selling Items'])
        writer.writerow(['Item Name', 'Total Quantity'])
        for item in context['top_selling_items']:
            writer.writerow([item['item__name'], item['total_quantity']])

        # Sales_by_category
        writer.writerow([]) 
        writer.writerow(['Sales by Category'])
        writer.writerow(['Category', 'Total Sales'])
        for category in context['sales_by_category']:
            writer.writerow([category['item__category__name'], category['total_sales']])

        # Sales report based on customer
        writer.writerow([]) 
        writer.writerow(['Sales by Customer'])
        writer.writerow(['Customer', 'Total Sales'])
        for customer in context['sales_by_customer']:
            writer.writerow([customer['customer__name'], customer['total_sales']])

        # Sales_by_time_of_day
        writer.writerow([])  
        writer.writerow(['Sales by Time of Day'])
        writer.writerow(['Hour', 'Total Sales'])
        for hour in context['sales_by_time_of_day']:
            writer.writerow([hour['hour'], hour['total_sales']])

        # Order_status_report
        writer.writerow([])  
        writer.writerow(['Order Status Report'])
        writer.writerow(['Status', 'Total Orders'])
        for status in context['order_status_report']:
            writer.writerow([status['status'], status['total_orders']])

        # Daily sales report
        writer.writerow([])  
        writer.writerow(['Daily Sales'])
        writer.writerow(['Date', 'Total Sales'])
        for day in context['daily_sales']:
            writer.writerow([day['date'], day['total_sales']])

        # Sales_by_employee_report
        writer.writerow([])
        writer.writerow(['Sales by Employee Report'])
        writer.writerow(['Employee', 'Total Sales'])
        for employee in context['sales_by_employee_report']:
            writer.writerow([employee['employee__name'], employee['total_sales']])
        
        # Customer_order_history_report
        writer.writerow([])
        writer.writerow(['Customer Order History Report'])
        writer.writerow(['Customer', 'Total Orders'])
        for customer in context['customer_order_history_report']:
            writer.writerow([customer['customer__name'], customer['total_orders']])
            return response
        
