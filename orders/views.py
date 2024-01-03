from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from .forms import UserSessionForm  , OrderForm
from django.contrib import messages
from cafe.models import Item
import json
from cafe.views import generate_random_id
from.models import Order , Discount
# from .models import Checkouts , Discount

# Create your views here.

class CheckoutView(View):
    template_name = 'checkout.html'  #Replace with the actual template file path
    model=Order    
    def get(self, request, *args, **kwargs):
        # Show the HTML form for GET requests
        form = OrderForm()  # Assuming you have a form for your Order model
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        # Process the form submission for POST requests
        form = OrderForm(request.POST)
        
        if form.is_valid():
            order_instance = form.cleaned_data
            session_data = request.session.get("order", {})
            order_dict = session_data.get("order", {})
            discount_data = request.session.get('discount', {})
            discount_price_reduction = discount_data.get('price_reduction', 0)
            original_price=0 # it should be calculate
            final_price = original_price - discount_price_reduction
            Order.objects.create(
                description="Your description here",
                table_number=order_instance["table_number"],
                order_detail=order_dict.get("item", []),
                customer_name=order_instance["Name"],
                phone_number=order_instance["phone_number"],
                discount_code=order_instance["discount_code"],
                order_id=order_dict.get("id"),
                final_price=final_price  
    )
            # Redirect to a success page or any other desired page
            return redirect('cafe:home')
        else:
            # Form data is invalid, render the form with errors
            return render(request, self.template_name, {'form': form})

# def apply_discount(request):
#     if request.method == 'POST':
#         form = DiscountCodeForm(request.POST)
#         if form.is_valid():
#             discount_code = form.cleaned_data['discount_code']
#             try:
#                 discount = Discount.objects.get(code=discount_code, valid_until__gte=timezone.now())

#                 # request.session['discount'] = {
#                 #     'code': discount.code,
#                 #     'price_reduction': discount.price_reduction
#                 # }
#                 return discount
#                 messages.success(request, 'Discount applied successfully!')
#             except Discount.DoesNotExist:
#                 messages.error(request, 'Invalid discount code or expired.')
#             return redirect('your_redirect_url')  # Replace with your actual redirect URL
#     else:
#         form = DiscountCodeForm()

#     return render(request, 'your_discount_template.html', {'form': form})
    

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
            


# class EditCookieView(View):
#     template_name = 'orders/edit_cart.html'

#     def get(self, request):
#             # Retrieve the cart data from the cookie
#             cart_data = request.COOKIES.get('cart', '{}')

#             # Process cart_data as needed
#             # ...

#             return render(request, self.template_name, {'cart_data': cart_data})

#     def post(self, request, category_name):
#         form = CartEditForm(request.POST)

#         if form.is_valid():
#             cd = form.cleaned_data

#             # Delete the previous cookie
#             response = HttpResponse()
#             response.delete_cookie('cart')

#             # Set new cookie
#             self.data[cd["iditem"]] = cd['quantity']
#             response.set_cookie("cart", f"{self.data}", expires=9)

#             # Delete previous session and add a new one
#             order = {"id": generate_random_id(), "item": self.data}
#             request.session.pop("order", None)
#             request.session["order"] = {"order": order, "status": ""}
            
#             # Redirect to the cart page
#             return redirect('orders:cart_page')

#         else:
#             # Print form errors to the console for debugging
#             print("Form errors:", form.errors)

#             return HttpResponse("Form is not valid. Check form.errors for details.")