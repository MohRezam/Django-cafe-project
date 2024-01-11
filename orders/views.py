from datetime import datetime, timedelta,date
from itertools import zip_longest
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse,HttpRequest
from django.shortcuts import redirect, render
from django.views import View
from .forms import UserSessionForm  , OrderForm ,CartAddForm , DiscountCodeForm
from django.contrib import messages
from cafe.models import Item, Cafe,Table
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
    discounted_number=0
    
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

        self.load_data_from_cookie(request)
        cafe = get_object_or_404(Cafe)
        form = OrderForm()
        cuppon_form = self.discount_form
        item_quantity_dict = self.data
        total_price = self.calculate_total_price(item_quantity_dict)
        self.model_total_price=total_price
        request.session['model_total_price'] = total_price

        if "code" in request.GET:
            discount_code = request.GET.get('code')
            discount_form = DiscountCodeForm(request.GET)
            discounted_number = self.apply_discount(request, discount_code)
            # Update self.model_discount_code using the value stored in the session
            self.model_discount_code = request.session.get('model_discount_code', None)
            request.session['final_price'] = discounted_number

            
            
        cart_items = Item.objects.filter(id__in=self.data.keys())
        values=(self.data.values())
        prices=self.calculate_price(self.data)
        combined_items = zip_longest(cart_items, values, prices, fillvalue=None)
        total_quantity=self.calculate_total_quantity(item_quantity_dict)
        if self.final_price == 0:
            final_price=total_price
        else:
            final_price= discounted_number
            self.final_price=final_price
        

            
        return render(request, self.template_name, {'form': form ,"combined_items":combined_items ,'total_price': total_price ,"total_quantity":total_quantity , "final_price":final_price,"discount":cuppon_form,"cafe":cafe})
    
    
    def get_final_price(self, request, *args, **kwargs):
        item_quantity_dict = self.data
        total_price = self.calculate_total_price(item_quantity_dict)
        if self.final_price == 0:
            final_price=total_price
        else:
            final_price= self.final_price
        
        return final_price

    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST)

        if form.is_valid():
            # discount_code = request.POST.get('discount_code')
            action = request.POST.get('action')
            describe= request.POST.get('description')
            table_number =request.POST.get('table_number')
            customer_name= request.POST.get('customer_name')
            phone_number = request.POST.get('phone_number')
            self.model_discount_code = request.session.get('model_discount_code', None)
            self.model_total_price = request.session.get('model_total_price', None)
            if action == 'checkout':
                return self.process_checkout(request, form , describe , table_number , customer_name , phone_number)
        self.model_discount_code = request.session.get('model_discount_code', None)
        return render(request, self.template_name, {'form': form})

    def apply_discount(self, request, discount_code):
            form = self.discount_form
            try:
                discount = Discount.objects.get(code=discount_code)
                print(discount)
            except Discount.DoesNotExist:
                messages.error(request, 'کد معتبر نمی باشد')
                return render(request, self.template_name, {'form': form})

            if discount.is_valid():
                request.session['model_discount_code'] = discount_code
                self.model_discount_code = discount_code
                amount = self.model_total_price
                discounted_amount = discount.apply_discount(amount)
                self.final_price = discounted_amount
                messages.success(request, 'کد تخفیف اعمال شد')
                return discounted_amount
            else:
                messages.error(request, 'کد تخفیف منقضی شده')
                return render(request, self.template_name, {'form': form})


    def process_checkout(self, request, form, describe, table_number, customer_name, phone_number):
        self.load_data_from_cookie(request)
        session_data = request.session.get("order", {})
        order_dict = session_data.get("order", {})
        cart_items = Item.objects.filter(id__in=self.data.keys())
        values = (self.data.values())
        prices = self.calculate_price(self.data)
        if self.final_price == 0:
            self.final_price = self.calculate_total_price(self.data)
        combined_items = zip_longest(cart_items, values, prices, fillvalue=None)
        food_items = []
        details_items = []
        for cart_item, quantity, price in combined_items:
            if cart_item is not None:
                item_name = cart_item.name
                item_price = cart_item.price
                item_id = cart_item.id
                food_item = {"name": item_name, "price": item_price, "quantity": quantity,"item_id":item_id}

                food_items.append(food_item)

        total_items = sum([int(item["quantity"]) for item in food_items])
        total_price = sum([int(item["price"]) * int(item["quantity"]) for item in food_items])

        details_item = {"total_item": total_items, "total_price": total_price}

        details_items.append(details_item)

        order_detail = {"food_items": food_items, "details_items": details_items}

        # Calculate final price based on the discount
        self.final_price = request.session.get('final_price', 0)
        if self.final_price == 0:
            self.final_price = self.calculate_total_price(self.data)
        if self.model_discount_code:
            final_price = self.final_price
        else:
            final_price = self.calculate_total_price(self.data)

        Order.objects.create(
            description=describe,
            table_number=Table.objects.get(table_number=table_number),
            order_detail=order_detail,
            customer_name=customer_name,
            phone_number=phone_number,
            discount_code=self.model_discount_code,
            order_id=order_dict.get("id", []),
            final_price=final_price,
        )
        messages.success(request,"سفارش شما با موفقیت ثبت شد","success")
        response = redirect('cafe:home')
        response.delete_cookie('cart')
        request.session.flush()
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
    cafe = get_object_or_404(Cafe)
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
        prices = [int(price) for price in prices]
        list_data = list(self.data.values())
        res_list = [prices[i] // list_data[i] for i in range(len(list_data))]
        combined_items = zip_longest(list_items.values(), values, prices,cart_items,res_list, fillvalue=None)

        return render(request, self.template_name, {'combined_items': combined_items,'cart_form':cart_form,'cafe':self.cafe})
    
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