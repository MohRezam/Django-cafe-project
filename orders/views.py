from django.shortcuts import render
from django.views import View
from .forms import UserSessionForm
from django.contrib import messages
# Create your views here.

class CheckoutView(View):
    def get(self, request):
        return render(request, "orders/checkout.html")
    

class CartView(View):
    form_class=UserSessionForm()
    def get(self, request):
        return render(request, "orders/cart.html")

    def post(self, request):
        form=self.form_class(request.POST)
        
        if form.is_valid():
            # Session.object.creat(phone_number)
            request.session['customer_phone']={
                "phone_number": form.cleaned_data['phone']
            }
        

# Create your views here.

# def add_order(request):
#     if request.method == "GET":
#         return render(request, "", context={})
    
    
# def checkout(request):
#     if request.method == "GET":
#         return render(request, "", context={})
    

# def cart(request):
#     if request.method == "GET":
#         return render(request, "", context={})
    

# from django.shortcuts import render
# from .models import Order
# def order_status(request, status):
#     try:
#         context = {
#         'order': status,
#             }   
#         request.session["order_status"]=context
#     except Order.DoesNotExist:
#         messages.error(request,'status doesnt confirm',"danger")
#         return None #change if need




# def order_status(request, order_id , status):
#     try:
#         order = Order.objects.get(id=order_id)
#         if order.is_completed:
#            status = "Completed"
#         else:
#             status = "In shopping cart"
#         context = {
#             'order': order,
#             'status':status
#         }
#         return render(request, 'order_status.html', context)
#     except Order.DoesNotExist:
#         return render(request, 'order_not_found.html')
            
# Mehdi Sadeghi was here and wrote this block of code
from django.shortcuts import render
from .models import Order
def order_status(request, order_id , status):
    try:
        order = Order.objects.get(id=order_id)
        context = {
        'order': order,
        'status':status
        }
        return render(request, 'order_status.html', context)
    except Order.DoesNotExist:
        return render(request, 'order_not_found.html')
            


