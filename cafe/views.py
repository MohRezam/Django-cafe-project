from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Item, Cafe
from django.views import View
from .forms import CartAddForm, SearchForm
from django.db.models import Q
# from django.shortcuts import render, redirect
# from django.views import View
# from .models import Order, OrderItem
# from .forms import OrderItemForm  
# Create your views here.


class HomeView(View):
    def get(self, request):
        cafe = get_object_or_404(Cafe)
        all_categories = Category.objects.all()        
        return render(request, "cafe/index.html", context={"all_categories":all_categories, "cafe":cafe})

class CafeMenuView(View):
    data = {}

    def dispatch(self, request, category_name):
        category = Category.objects.filter(category_name=category_name).exists()
        if not category:
            return redirect("cafe:home")
        return super().dispatch(request, category_name)

    def get(self, request, category_name):
        cart_form = CartAddForm()
        cafe = get_object_or_404(Cafe)
        items = Item.objects.filter(category=category_name)
        search_form = SearchForm()
        if "search" in request.GET:
            search_form = SearchForm(request.GET)
            if search_form.is_valid():
                cd = search_form.cleaned_data["search"]
                items = Item.objects.filter(Q(name__icontains=cd) | Q(price__icontains=cd), category=category_name)
        return render(request, "cafe/menu-item.html", context={"items": items, "cart_form": cart_form, "cafe":cafe, "search_form":search_form})

    def post(self, request, category_name):
        form = CartAddForm(request.POST)
        
        if form.is_valid():
            cd = form.cleaned_data
            self.data[cd["iditem"]] = cd['quantity']  
            order = {"id": generate_random_id(), "item": self.data}
            response = redirect('orders:cart_page')
            response.set_cookie("cart", f"{self.data}", expires=9)
            request.session["order"] = {"order": order, "status": ""}
            return response
        else:
            # Print form errors to the console for debugging
            print("Form errors:", form.errors)
            
            return HttpResponse("Form is not valid. Check form.errors for details.")
        
# class CafeMenuView(View):
#     data = {}

#     def dispatch(self, request, category_name):
#         category = Category.objects.filter(category_name=category_name).exists()
#         if not category:
#             return redirect("cafe:home")
#         return super().dispatch(request, category_name)

#     def get(self, request, category_name):
#         cart_form = CartAddForm()
#         cafe = get_object_or_404(Cafe)
#         items = Item.objects.filter(category=category_name)
#         search_form = SearchForm()
#         if "search" in request.GET:
#             search_form = SearchForm(request.GET)
#             if search_form.is_valid():
#                 cd = search_form.cleaned_data["search"]
#                 items = Item.objects.filter(Q(name__icontains=cd) | Q(price__icontains=cd), category=category_name)
#         return render(
#             request,
#             "cafe/menu-item.html",
#             context={"items": items, "cart_form": cart_form, "cafe": cafe, "search_form": search_form},
#         )

#     def post(self, request, category_name):
#         form = CartAddForm(request.POST)

#         if form.is_valid():
#             cd = form.cleaned_data
#             self.data[cd["iditem"]] = cd['quantity']
#             order = {"id": generate_random_id(), "item": self.data}
#             request.session.setdefault("cart", {}).update(self.data)
#             request.session["order"] = {"order": order, "status": ""}
#             return redirect('orders:cart_page')
#         else:
#             # Print form errors to the console for debugging
#             print("Form errors:", form.errors)

#             return HttpResponse("Form is not valid. Check form.errors for details.")

import uuid

def generate_random_id():
    return str(uuid.uuid4())



        


class AboutUsView(View):
    def get(self, request):
        cafe = get_object_or_404(Cafe)
        return render(request, "cafe/about.html", {"cafe":cafe})


class ContactUsView(View):
    def get(self, request):
        cafe = get_object_or_404(Cafe)
        return render(request, "cafe/contact-us.html", {"cafe":cafe})
#in zir
class SetCartCookieView(View):
    def get(self, request):
        cart_data = "your_cart_data_here"  # Replace this with your actual cart data
        response = HttpResponse("Cookie set successfully")
        response.set_cookie('cart', cart_data, max_age=3600)  # 'max_age' sets the cookie's expiration time in seconds

        # Optionally, you can set other attributes for the cookie
        # response.set_cookie('cart', cart_data, max_age=3600, secure=True, httponly=True, samesite='Strict')

        return response
class AddToCartView(View):
    def get(self, request, item_id):
        cart = request.COOKIES.get('cart', '').split(',')  # Get cart data from cookies
        cart.append(str(item_id))  # Add the new item to the cart
        response = redirect('menu')
        response.set_cookie('cart', ','.join(cart))  # Update the cart in cookies

        # Store cart data in session for tracking
        request.session['cart'] = cart
        return response

class ViewCartView(View):
    def get(self, request):
        cart_item_ids = request.COOKIES.get('cart')
        print("print",cart_item_ids)
        cart_items = Item.objects.filter(id__in=cart_item_ids.keys())
        return render(request, 'orders/cart.html', {'cart_items': cart_items, "quantity": cart_item_ids})


class CheckoutView(View):
    def get(self, request):
        cart_item_ids = request.session.get('cart', [])  # Get cart data from session
        # Fetch cart items from the database using cart_item_ids
        cart_items = Item.objects.filter(id__in=cart_item_ids)

        # Process checkout logic here
        # For example, save the order, clear the cart, etc.

        # Clear the cart after checkout by expiring the cookie and deleting session data
        response = HttpResponse('Checkout successful!')
        response.delete_cookie('cart')
        del request.session['cart']
        return response



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


    

