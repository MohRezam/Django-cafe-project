from django.shortcuts import render, redirect , get_object_or_404
from .forms import UserLoginForm,UserForm,UserChangeForm,CategoryForm,CategoryChangeForm,ItemForm,SortOrdersPhone,ChangeOrderForm,CreateOrderForm
from django.views import View
from cafe.models import Item,Category
from accounts.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login,authenticate,logout
from django.views.generic import TemplateView
from django.db.models import Count, Sum,Q,F,DateTimeField
from django.utils import timezone
from orders.models import Order
import csv,json
from collections import Counter
from django.http import HttpResponse,JsonResponse
import calendar
from calendar import month_name
from datetime import datetime, date,timedelta




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
                return redirect('accounts:staff-profile')
            messages.error(request, 'این شماره تلفن یا رمز عبور درست نمی باشد', 'warning')
        return render(request, self.template_name, {'form': form})
    
class StffLogoutView(LoginRequiredMixin, View):
	def get(self, request):
		logout(request)
		messages.success(request, 'خروج موفقیت آمیز انجام شد', 'success')
		return redirect('accounts:staff-login')





        
class StffProfileView(LoginRequiredMixin, View):
    def get(self, request):
        last_five_orders = Order.objects.order_by('-created_at')[:5]
        all_orders = Order.objects.filter(order_status=True).exclude(order_detail=None).values_list('order_detail', flat=True)
        product_id = [item['food_items'][0]['item_id'] for item in all_orders]
        counter = Counter(product_id)
        most_common_3 = counter.most_common(3)
        list_product_popular = []
        for pro_id in most_common_3:
            list_product_popular.append(Item.objects.filter(id=pro_id[0]))
        today = date.today()
        today_salse = timezone.now().date()
        current_date = datetime.now()
        orders_today = Order.objects.filter(order_date__date=today_salse).count()
        unpaid_orders = Order.objects.filter(order_date__date=today_salse,order_status=False).count()
        paid_orders = Order.objects.filter(order_date__date=today_salse,order_status=True).count()
        today_salse = Order.objects.filter(order_date__date=today_salse, order_status=True).aggregate(total=Sum('final_price'))
        one_month_ago = today - timedelta(days=30)
        orders_in_range = Order.objects.filter(order_status=True,order_date__date__gte=one_month_ago, order_date__date__lte=today)
        total_sales_in_range = orders_in_range.aggregate(total_sales=Sum('final_price'))
        total_sales_amount = total_sales_in_range['total_sales'] if total_sales_in_range['total_sales'] is not None else 0
        one_year_ago = current_date - timedelta(days=365)
        orders_annual = Order.objects.filter(order_status=True,order_date__date__gte=one_year_ago, order_date__date__lte=current_date)
        total_sales_annual = orders_annual.aggregate(total_sales=Sum('final_price'))
        total_sales_amount_annual = total_sales_annual['total_sales'] if total_sales_annual['total_sales'] is not None else 0
        order_reports = [orders_today,unpaid_orders,paid_orders]
        salse_reports = [today_salse,total_sales_amount,total_sales_amount_annual]
        return render(request, 'accounts/profile.html', {"orders": last_five_orders,"orders_tody":order_reports,"salse_report":salse_reports,"pupolar_product":list_product_popular})
     

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
            messages.success(request, 'آپدیت اطلاعات کاربر با موفقیت انجام شد', 'success')
            return redirect('accounts:staff-list-user')
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
    form_class = CategoryChangeForm
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
    form_class = CategoryChangeForm
    template_name = "accounts/profile-add-category.html"
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
        
    def post(self, request):
        form = self.form_class(request.POST,request.FILES)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'آپدیت اطلاعات شخصی با موفقیت انجام شد', 'success')
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
class StaffProfileUpdateItemView(LoginRequiredMixin,View):
     form_class = ItemForm
     template_name = "accounts/profile-update-item.html"
     def get(self,request,id_item) :
        item = get_object_or_404(Item, id=id_item)
        form = self.form_class(instance=item)
        return render(request, self.template_name, {'form': form})
     
     def post(self,request,id_item):
        item = get_object_or_404(Item, id=id_item)
        form = self.form_class(request.POST,request.FILES,instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'آپدیت محصول با موفقیت انجام شد', 'success')
            return redirect('accounts:staff-items')
        else:
            form = self.form_class(instance=item)
            return render(request, self.template_name, {'form': form})  
class StaffProfileAddItemView(LoginRequiredMixin,View):
     form_class = ItemForm
     template_name = "accounts/profile-add-item.html"
     def get(self,request,) :
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
     
     def post(self,request):
        form = self.form_class(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'آفزودن محصول با موفقیت انجام شد', 'success')
            return redirect('accounts:staff-items')
        else:
            form = self.form_class()
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
class StaffProfileOrdersView(LoginRequiredMixin, View):
    form_class = SortOrdersPhone
    template_name = 'accounts/orders.html'

    def get(self, request):
        form = self.form_class()
        order = Order.objects.all()
        
        if "search" in request.GET:
            form = self.form_class(request.GET)
            if form.is_valid():  
                cd = form.cleaned_data["search"]
                order = Order.objects.filter(
                    Q(customer_name__icontains=cd) |
                    Q(phone_number__icontains=cd) |
                    Q(table_number__exact=cd) |
                    Q(staff_id__exact=cd) |
                    Q(final_price__icontains=cd)
                )
        return render(request, self.template_name, {"orders": order, "form": form})  
class StaffProfileOrderUncompleteView(LoginRequiredMixin,View):
    def get(self,request):
          order = Order.objects.filter(order_status=False)
          return render(request,'accounts/orders-uncomplete.html',{"orders":order})
class StaffProfileOrdercompleteView(LoginRequiredMixin,View):
    def get(self,request):
          order = Order.objects.filter(order_status=True)
          return render(request,'accounts/orders-complete.html',{"orders":order})
class StaffProfileOrderDetailView(LoginRequiredMixin,View):
    def get(self,request,id_order):
        order = Order.objects.get(id=id_order)
        return render(request,'accounts/profile-order-details.html',{"order":order})
class StaffReportsInsightsView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'accounts/profile-reports-insight.html')
class StaffChangeOrderView(LoginRequiredMixin, View):
    form_class = ChangeOrderForm
    template_name = "accounts/profile-update-order.html"

    def get(self, request, id_order):
        order = get_object_or_404(Order, id=id_order)
        form = self.form_class(instance=order)
        return render(request, self.template_name, {"form": form})

    def post(self, request, id_order):
        order = get_object_or_404(Order, id=id_order)
        form = self.form_class(request.POST, request.FILES, instance=order)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'آپدیت سفارش با موفقیت انجام شد')
            return redirect('accounts:staff-orders')
        else:
            messages.error(request, 'خطا در فرم، لطفاً مجدداً تلاش کنید')
            return render(request, self.template_name, {'form': form}) 
class StaffAddOrderView(LoginRequiredMixin,View):
    form_class = CreateOrderForm
    template_name = 'accounts/profile-add-order.html'  

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            messages.success(request,"سفارش با موفقیت ثبت شد")
            return redirect('accounts:staff-orders')  
        messages.error(request,"لطفا در تکمیل فیلد ها دقت فرمایید")
        return render(request, self.template_name, {'form': form})
class StaffDeleteOrderView(LoginRequiredMixin,View):
        def get(self,request,order_id):
          order = get_object_or_404(Order, pk=order_id)
          order.delete()
          messages.success(request,"سفارش با موفقیت حذف شد","success")
          return redirect("accounts:staff-orders")
class StaffUserView(LoginRequiredMixin,View):
       def get(self,request):
          if request.user.is_admin:
            user = User.objects.all()
            return render(request,'accounts/profile-list-user.html',{"user":user})
          redirect("accounts:staff-profile")
          
class staffUserDeleteView(LoginRequiredMixin,View):
    def get(self,request,id_user):
        if request.user.is_admin:
            user = get_object_or_404(User, pk=id_user)
            user.delete()
            messages.success(request,"حذف کاربر با موفقیت انجام شد","success")
            return redirect("accounts:staff-list-user")
        redirect("accounts:staff-profile")