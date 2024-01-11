from django.shortcuts import render, redirect , get_object_or_404
from .forms import UserLoginForm,UserForm,UserChangeForm,CategoryForm,CategoryChangeForm,ItemForm,SortOrdersPhone,ChangeOrderForm,CreateOrderForm,TableForm,CafeForm
from django.views import View
from cafe.models import Item,Category,Table
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
from datetime import datetime, date,timedelta
from django.views import View
from django.http import JsonResponse
from django.db.models import Sum, Count
from django.db.models.functions import TruncHour
from collections import Counter




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
        list_category_popular = []
        for pro_id in most_common_3:
            list_product_popular.append(Item.objects.filter(id=pro_id[0]))
            list_category_popular.append(Item.objects.get(id=pro_id[0]).category)
        top_selling_staff = Order.objects.values('staff_id').annotate(order_count=Count('staff_id'), total_sales=Sum('final_price')).order_by('-total_sales').first()
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
        return render(request, 'accounts/profile.html', {"orders": last_five_orders,"orders_tody":order_reports,"salse_report":salse_reports,"pupolar_product":list_product_popular,"list_category_popular":list_category_popular,"top_selling_staff":top_selling_staff})
     

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
            instance = form.save(commit=False)
            # Do any additional processing if needed before saving
            instance.save()
            messages.success(request, 'عملیات با موفقیت انجام شد', 'success')
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
class StatisticsMixin:
    @staticmethod
    def fetch_data():
        # Common data fetching logic used in both views
        # You can modify this based on your actual data fetching requirements
        end_date = timezone.now()
        start_date = end_date - timedelta(days=365)
        monthly_sales_amount = Order.objects.filter(order_status=True,order_date__range=(start_date, end_date)).values('order_date__month').annotate(sales_amount=Sum('final_price')).order_by('order_date__month')
        time_of_day_sales = Order.objects.annotate(hour=TruncHour('order_date')).values('hour').annotate(total_orders=Count('id'), total_sales=Sum('final_price'))
        employee_sales = Order.objects.values('staff_id').annotate(total_sales=Sum('final_price'))
        # Ensure the keys are present in the result

        employee_sales = [{'staff_id': sale.get('staff_id', 'Unknown Employee'), 'total_sales': sale['total_sales']} for sale in employee_sales]

        # Convert QuerySet to list for time_of_day_sales
        time_of_day_sales = list(time_of_day_sales)

        return {
            "monthly_sales_amount":monthly_sales_amount,
            "time_of_day_sales": time_of_day_sales,
            "employee_sales": employee_sales,
        }
class DownloadCSVView(View, StatisticsMixin):
    model = Order
    template_name = "accounts/csv.html"
    def get(self, request, *args, **kwargs):
        data = self.fetch_data()

        # Prepare CSV data
        csv_data = self.prepare_csv_data(data)

        # Create a CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sales_statistics.csv"'

        writer = csv.writer(response)

        # Write CSV data
        writer.writerows(csv_data)

        return response

    def prepare_csv_data(self, data):
        csv_data = []
        csv_data.extend([['month', 'Total Orders']])
        csv_data.extend([[sale['order_date__month'], sale['sales_amount']] for sale in data['monthly_sales_amount']])
        csv_data.append([]) 


        # Write CSV headers for time of day sales
        csv_data.extend([['Hour', 'Total Orders', 'Total Sales']])
        csv_data.extend([[sale['hour'], sale['total_orders'], sale['total_sales']] for sale in data['time_of_day_sales']])
        csv_data.append([])  # Add an empty row for better readability

        # Write CSV headers for employee sales
        csv_data.extend([['Staff ID', 'Total Sales']])
        csv_data.extend([[sale['staff_id'], sale['total_sales']] for sale in data['employee_sales']])

        return csv_data


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
        end_date = timezone.now()
        start_date = end_date - timedelta(days=365)

        monthly_orders_count = Order.objects.filter(order_status=True,order_date__range=(start_date, end_date)).values('order_date__month').annotate(order_count=Count('id')).order_by('order_date__month')
        labels_month_order = [0]*12
        for item in monthly_orders_count:
            labels_month_order[item['order_date__month']-1] = item['order_count']
        monthly_sales_amount = Order.objects.filter(order_status=True,order_date__range=(start_date, end_date)).values('order_date__month').annotate(sales_amount=Sum('final_price')).order_by('order_date__month')
        labels_month_amount = [0]*12
        for entry in monthly_sales_amount:
            labels_month_amount[entry['order_date__month']-1] = entry['sales_amount']

        start_date = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = timezone.now()

        daily_orders_count = Order.objects.filter(order_status=True,
                                                  order_date__range=(start_date, end_date)).values('order_date__day').annotate(order_count=Count('id')).order_by('order_date__day')
        label_daily_order = [0]*30
        for order in daily_orders_count:
            label_daily_order[order['order_date__day']-1] = order['order_count']
        
        daily_orders_amount = Order.objects.filter(order_status=True,
                                                  order_date__range=(start_date, end_date)).values('order_date__day').annotate(sales_amount=Sum('final_price')).order_by('order_date__day')
        label_daily_amount = [0]*30
        for order in daily_orders_amount:
            label_daily_amount[order['order_date__day']-1] = order['sales_amount']
        
        start_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = timezone.now()

        hourly_orders_count = Order.objects.filter(order_status=True,order_date__range=(start_date, end_date)).values('order_date__hour').annotate(order_count=Count('id')).order_by('order_date__hour')
        label_hour_orders_count = [0]*24
        for entry in hourly_orders_count:
            label_hour_orders_count[entry['order_date__hour']] = entry['order_count']
        hourly_orders_count = Order.objects.filter(order_status=True,order_date__range=(start_date, end_date)).values('order_date__hour').annotate(sales_amount=Sum('final_price')).order_by('order_date__hour')
        label_hour_orders_amount = [0]*24
        for entry in hourly_orders_count:
            label_hour_orders_amount[entry['order_date__hour']] = entry['sales_amount']
        return render(request, 'accounts/profile-reports-insight.html',{'labels_month_order':labels_month_order,'labels_month_amount':labels_month_amount,'label_daily_order':label_daily_order,'label_daily_amount':label_daily_amount,'label_hour_orders_count':label_hour_orders_count,'label_hour_orders_amount':label_hour_orders_amount })
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
          
class StaffUserDeleteView(LoginRequiredMixin,View):
    def get(self,request,id_user):
        if request.user.is_admin:
            user = get_object_or_404(User, pk=id_user)
            user.delete()
            messages.success(request,"حذف کاربر با موفقیت انجام شد","success")
            return redirect("accounts:staff-list-user")
        redirect("accounts:staff-profile")
class StaffTablesView(LoginRequiredMixin,View):
      def get(self,request):
          tables = Table.objects.all()
          return render(request,"accounts/profile-list-table.html",{"tables":tables})
class StaffDeleteTableView(LoginRequiredMixin,View):
    def get(self,request,id_table):
        if request.user.is_admin:
            table = Table.objects.get(id=id_table)
            table.delete()
            messages.success(request,"حذف میز با موفقیت انجام شد","success")
            return redirect("accounts:staff-list-table")
        redirect("accounts:staff-profile")


class StaffTableFormView(LoginRequiredMixin,View):
    def get(self, request,id_table):
        table = get_object_or_404(Table,id=id_table)
        form = TableForm(instance=table)
        return render(request, 'accounts/prfile-edite-table.html', {'form': form})

    def post(self, request,id_table):
        table = get_object_or_404(Table,id=id_table)
        form = TableForm(request.POST,instance=table)
        if form.is_valid():
            table.save()
            return redirect("accounts:staff-list-table")
        return render(request, 'accounts/prfile-edite-table.html', {'form': form})  
class StaffOptionsView(LoginRequiredMixin,View):
    form_class = CafeForm
    tempalte_name = "accounts/profile-options.html"
    def get(self,request):
        form = self.form_class
        return render(request,self.tempalte_name,{'form':form})
    def post(self,request):
        form = self.form_class(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"تنظیمات با موفقیت ذخیره شود")
            redirect("accounts:staff-profile")
        return render(request,self.tempalte_name,{'form':form})
