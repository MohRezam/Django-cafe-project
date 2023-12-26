from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Item
from django.views import View
# from django.shortcuts import render, redirect
# from django.views import View
# from .models import Order, OrderItem
# from .forms import OrderItemForm  
# Create your views here.


class HomeView(View):
    def get(self, request):
        all_categories = Category.objects.all()        
        return render(request, "cafe/index.html", context={"all_categories":all_categories})

class CafeMenuView(View):
    def dispatch(self, request, category_name):
        category = Category.objects.filter(category_name=category_name).exists()
        if not category:
            return redirect("cafe:home")
        return super().dispatch(request, category_name)
    
    def get(self, request, category_name):
        items = Item.objects.filter(category=category_name)
        return render(request, "cafe/menu-item.html", context={"items":items})


class AboutUsView(View):
    def get(self, request):
        return render(request, "cafe/about.html", {})


class ContactUsView(View):
    def get(self, request):
        return render(request, "cafe/contact-us.html", {})




# class CartView(View):
#     def get(self, request):
#         return render(request, "cafe/cart.html")    

# class AddOrderView(View):
#     def get(self, request):
#         form = OrderItemForm()  
#         return render(request, "add_order.html", context={'form': form})
    
#     def post(self, request):
#         form = OrderItemForm(request.POST)
#         if form.is_valid():
#             order_id = request.session.get('order_id')
#             if order_id:
#                 order = Order.objects.get(pk=order_id)
#             else:
#                 order = Order.objects.create(customer=request.user.customer) 
            
#             item = form.cleaned_data['item']
#             quantity = form.cleaned_data['quantity']
#             order_item, created = OrderItem.objects.get_or_create(order=order, item=item)
#             if not created:
#                 order_item.quantity += quantity
#                 order_item.save()
            
#             request.session['order_id'] = order.id
#             return redirect('cart')
        
#         return render(request, "add_order.html", context={'form': form})

# class CartView(View):
#     def get(self, request):
#         order_id = request.session.get('order_id')
#         if order_id:
#             order = Order.objects.get(pk=order_id)
#             order_items = OrderItem.objects.filter(order=order)
#         else:
#             order = None
#             order_items = None
#         return render(request, "cart.html", context={'order': order, 'order_items': order_items})

# class CheckoutView(View):
#     def get(self, request):
#         order_id = request.session.get('order_id')
#         if order_id:
#             order = Order.objects.get(pk=order_id)
#             del request.session['order_id']
#             return render(request, "checkout.html", context={'order': order})
#         else:
#             return redirect('cart')

#     def post(self, request):
#         order_id = request.session.get('order_id')
#         if order_id:
#             order = Order.objects.get(pk=order_id)
#             #........
            
#             del request.session['order_id']
#             return redirect('success')  
#         else:
#             return redirect('cart')

    
