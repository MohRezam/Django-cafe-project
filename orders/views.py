from django.shortcuts import render
from django.views import View
from .forms import UserSessionForm
from django.contrib import messages
from cafe.models import Item
import json
# from .models import Checkouts , Discount

# Create your views here.

class CheckoutView(View):
    # model = Checkouts
    # model_1= Discount
    def get(self, request):
        return render(request, "orders/checkout.html")
    
    # def post(self, request):
    #         form = CheckoutForm(request.POST)
    #         if form.is_valid():
    #             cd = form.cleaned_data
    #             discount_code_result= any(self.model_1.objects.get(code=cd["discount_code"]))
    #             if discount_code_result is True:
                    #    ...
    #                 self.model.objects.create (name=cd["name"] , phone_number= cd["phone_number"] , order_id= ... , table_number=cd["table_number"] , discountـcode="discountـcode" )
    #                 messages.success(request , "با موفقیت ثبت شد" , "success")
    #             else:

    #             return response
    #         else:
    #             # Print form errors to the console for debugging
    #             print("Form errors:", form.errors)
                
    #             return HttpResponse("Form is not valid. Check form.errors for details.")

    

class ViewCartView(View):
    def get(self, request):
        cart_item_ids = request.COOKIES.get('cart')
        cart_item_ids=eval(cart_item_ids)
        cart_items = Item.objects.filter(id__in=cart_item_ids.keys())
        value=(cart_item_ids.values())
        values=(*value,)
        # def cart_summary(request):
        #     # Get the cart
        #     cart = Cart(request)
        #     cart_products = cart.get_quants
        #     totals = cart.cart_total()
        #     return render(request, "cart_summary.html", { 'cart_products':cart.get_quants, 'quantities':quantities, 'totals':totals})
        # def cart_total(self):
        #     # Get product IDS
        #         product_ids = self.cart.keys()
        #         # lookup those keys in our products database model
        #         products = Product.objects.filter(id__in=product_id)
        #         # Get quantities
        #         quantites = self.cart_total
        #         # start counting at 0
        #         total = 0
        #         for key, values in quantities.items():
        #             # Convert key string into int so we can do math
        #             key = int(key)
        #             for product in products:
        #                 if product.id == key:
        #                 total = total + (product.price * value)
                        # else:
                        #     total = total + (product.price * value)
        
        return render(request, 'orders/cart.html', {'cart_items': cart_items, "quantity":values[0]})


        

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
            


