from datetime import datetime, timedelta,date
from itertools import zip_longest
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse,HttpRequest
from django.shortcuts import redirect, render
from django.views import View
from .forms import UserSessionForm  , OrderForm ,CartAddForm , DiscountCodeForm
from django.contrib import messages
from cafe.models import Item
import json
from cafe.views import generate_random_id
from.models import Order ,Discount
from django.shortcuts import get_object_or_404
from .models import Item



class CheckoutView(View):
    template_name = 'orders/checkout.html'
    model = Order
    discount_form = DiscountCodeForm
    data = {}
    final_price= 0
    model_discount_code= None
    total_price=0
    model_total_price = 0
    
    def dispatch(self, request: HttpRequest, *args: any, **kwargs: any) -> HttpResponse:
            if len(self.load_data_from_cookie(request)) == 0:
             return redirect("cafe:home")
            return super().dispatch(request, *args, **kwargs)

    def load_data_from_cookie(self, request):
        cart_cookie = request.COOKIES.get('cart', '{}')
        try:
            self.data = json.loads(cart_cookie)
        except json.JSONDecodeError:
            self.data = {}
        return self.data

    def get(self, request, *args, **kwargs):
        # if "code" in request.GET:
        #     discount_code = request.GET.get('discount_code')
        #     discount_form = DiscountCodeForm(request.GET)
        #     if discount_form.is_valid():
        #         return self.apply_discount(request, discount_code)
        self.load_data_from_cookie(request)
        form = OrderForm()
        cuppon_form = self.discount_form
        item_quantity_dict = self.data
        total_price = self.calculate_total_price(item_quantity_dict)
        self.model_total_price=total_price
        cart_items = Item.objects.filter(id__in=self.data.keys())
        values=(self.data.values())
        prices=self.calculate_price(self.data)
        combined_items = zip_longest(cart_items, values, prices, fillvalue=None)
        total_quantity=self.calculate_total_quantity(item_quantity_dict)
        if self.final_price == 0:
            final_price=total_price
        else:
            final_price= self.final_price
            
        return render(request, self.template_name, {'form': form ,"combined_items":combined_items ,'total_price': total_price ,"total_quantity":total_quantity , "final_price":final_price,"discount":cuppon_form})

    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST)

        if form.is_valid():
            # discount_code = request.POST.get('discount_code')
            action = request.POST.get('action')
            describe= request.POST.get('describe')
            table_number =request.POST.get('table_number')
            customer_name= request.POST.get('customer_name')
            phone_number = request.POST.get('phone_number')
            if action == 'checkout':
                print("checkout-----")
                return self.process_checkout(request, form , describe , table_number , customer_name , phone_number)

        return render(request, self.template_name, {'form': form})

    def apply_discount(self, request, discount_code):
        form = self.discount_form
        try:
            discount =  Discount.objects.get(code=discount_code)
        except Discount.DoesNotExist:
            return render(request, self.template_name, {'form': form, 'error_message': 'Invalid discount code'})

        if discount.is_valid():
            self.model_discount_code= discount_code
            amount = self.total_price
            discounted_amount = discount.apply_discount(amount)
            self.total_price = discounted_amount
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return render(request, self.template_name, {'form': form, 'error_message': 'Discount code has expired'})


    def process_checkout(self, request, form , describe , table_number , customer_name , phone_number):
        self.load_data_from_cookie(request)
        session_data = request.session.get("order", {})
        order_dict = session_data.get("order", {})
        cart_items = Item.objects.filter(id__in=self.data.keys())
        values=(self.data.values())
        prices=self.calculate_price(self.data)
        if self.final_price == 0:
            self.final_price = self.calculate_total_price(self.data)
        combined_items = zip_longest(cart_items, values, prices, fillvalue=None)
        food_items = []
        details_items = []
        for cart_item, quantity, price in combined_items:
            if cart_item is not None:
                item_name = cart_item.name
                item_price = cart_item.price

                food_item = {"name": item_name, "price": item_price, "quantity": quantity}

                food_items.append(food_item)
        

        total_items = sum([item["quantity"] for item in food_items])
        total_price = sum([item["price"] * item["quantity"] for item in food_items])

        details_item = {"total_item": total_items, "total_price": total_price}

        details_items.append(details_item)

        order_detail = {"food_items": food_items, "details_items": details_items}

        

        Order.objects.create(
            description=describe,
            table_number=table_number,
            order_detail=order_detail,
            customer_name=customer_name,
            phone_number=phone_number,
            discount_code=self.model_discount_code,
            order_id=order_dict.get("id", []),
            final_price=self.final_price,
        )
        
        response = redirect('cafe:home')
        response.delete_cookie('cart')
        request.session.delete('order')
        return response
    
    def calculate_price(self,item_quantity_dict):
        total_price = 0
        price_list=[]

        for item_id, quantity in item_quantity_dict.items():
            item = get_object_or_404(Item, id=item_id)
            item_price = item.price
            total_price = item_price * int(quantity)
            price_list.append(total_price)

        return price_list
    
    def calculate_total_price(self,item_quantity_dict):
        total_price = 0

        for item_id, quantity in item_quantity_dict.items():
            item = get_object_or_404(Item, id=item_id)
            item_price = item.price
            total_price += item_price * int(quantity)

        return total_price
    
    def calculate_total_quantity(self , item_quantity_dict):
        total_quantity=0

        for _, quantity in item_quantity_dict.items():
            total_quantity +=int(quantity)

        return total_quantity


class ViewCartView(View):
    template_name='orders/cart.html'
    data = {}
    def dispatch(self, request: HttpRequest, *args: any, **kwargs: any) -> HttpResponse:
            if len(self.load_data_from_cookie(request)) == 0:
             return redirect("cafe:home")
            return super().dispatch(request, *args, **kwargs)
    def load_data_from_cookie(self, request):
        cart_cookie = request.COOKIES.get('cart', '{}')
        try:
            print(cart_cookie)
            self.data = json.loads(cart_cookie)
        except json.JSONDecodeError:
            self.data = {}
        return self.data

    def save_data_to_cookie(self, response):
        expiration_date = datetime.now() + timedelta(days=365)
        response.set_cookie("cart", json.dumps(self.data), expires=expiration_date)

    def save_data_to_session(self, request):
        request.session['cart'] = self.data

    def get(self, request):
        self.load_data_from_cookie(request)
        cart_form = CartAddForm()
        cart_items = Item.objects.filter(id__in=self.data.keys())
        list_items = {}
        for item in self.data.keys():
            list_items[item] = Item.objects.filter(id=int(item))

        values=(self.data.values())
        prices=self.calculate_price(self.data)
        combined_items = zip_longest(list_items.values(), values, prices,cart_items, fillvalue=None)

        return render(request, self.template_name, {'combined_items': combined_items,'cart_form':cart_form})
    
    def post(self, request, *args, **kwargs):
        self.load_data_from_cookie(request)
        form = CartAddForm(request.POST)
        if form.is_valid():
            item_id = request.POST.get('item_id')
            quantity = request.POST.get('quantity')
            action = request.POST.get('action')
            if action == 'delete':

                self.data.pop(item_id)

                self.save_data_to_session(request)   

                response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))   

                self.save_data_to_cookie(response)

                return response
            
            elif action == 'save':
                self.save(item_id, quantity)
                
                response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
                
                self.save_data_to_cookie(response)

                
                return response
        else:
            print("Form errors:", form.errors)
            return HttpResponse("Form is not valid. Check form.errors for details.")


    def save(self,item_id, quantity ):
        self.data[item_id] = int(quantity)
        order = {"id": generate_random_id(), "item": self.data}
        self.request.session["order"] = {"order": order, "status": ""}
        print(f"Saving item {item_id} with quantity {quantity}")
        
    def calculate_price(self,item_quantity_dict):
        total_price = 0
        price_list=[]

        for item_id, quantity in item_quantity_dict.items():
            item = get_object_or_404(Item, id=item_id)
            item_price = item.price
            total_price = item_price * int(quantity)
            price_list.append(total_price)

        return price_list