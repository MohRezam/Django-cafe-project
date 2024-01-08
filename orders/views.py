from datetime import datetime, timedelta
from itertools import zip_longest
from typing import Any
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from .forms import UserSessionForm  , OrderForm ,CartAddForm , DiscountCodeForm
from django.contrib import messages
from cafe.models import Item, Cafe
import json
from cafe.views import generate_random_id
from .models import Order ,Discount
from django.shortcuts import get_object_or_404
from .models import Item


class CheckoutView(View):
    """
    A class-based view for handling the checkout process.

    Attributes:
        template_name (str): The name of the template to render.
        model (class): The model class associated with the view.
        discount_form (class): The form class for discount codes.
        data (dict): The data dictionary for storing cart items.
        final_price (float): The final price of the order.
        model_discount_code (str): The discount code applied to the order.
        total_price (float): The total price of the order.

    Methods:
        load_data_from_cookie(request): Loads cart data from cookies.
        get(request, *args, **kwargs): Handles GET requests.
        post(request, *args, **kwargs): Handles POST requests.
        apply_discount(request, discount_code): Applies a discount to the order.
        process_checkout(request, form, describe, table_number, customer_name, phone_number): Processes the checkout and creates an order.
        calculate_price(item_quantity_dict): Calculates the price for each item in the cart.
        calculate_total_price(item_quantity_dict): Calculates the total price of the order.
        calculate_total_quantity(item_quantity_dict): Calculates the total quantity of items in the cart.
    """
    template_name = 'orders/checkout.html'
    model = Order
    discount_form = DiscountCodeForm
    data = {}
    final_price= 0
    model_discount_code= None
    total_price=0
    
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if len(self.load_data_from_cookie(request)) == 0:
            return redirect("cafe:home")
        return super().dispatch(request, *args, **kwargs)
    
    def load_data_from_cookie(self, request):
        """
        Loads cart data from cookies.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            None
        """
        cart_cookie = request.COOKIES.get('cart', '{}')
        try:
            self.data = json.loads(cart_cookie)
        except json.JSONDecodeError:
            self.data = {}
        
        return self.data

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: The HTTP response object.
        """
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
        """
        Handles POST requests.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: The HTTP response object.
        """
        form = OrderForm(request.POST)

        if form.is_valid():
            # discount_code = request.POST.get('discount_code')
            action = request.POST.get('action')
            describe= request.POST.get('describe')
            table_number =request.POST.get('table_number')
            customer_name= request.POST.get('name')
            phone_number = request.POST.get('phone_number')
            if action == 'checkout':
                print("checkout-----")
                return self.process_checkout(request, form , describe , table_number , customer_name , phone_number)

        return render(request, self.template_name, {'form': form})

    def apply_discount(self, request, discount_code):
        """
        Applies a discount to the order.

        Args:
            request (HttpRequest): The HTTP request object.
            discount_code (str): The discount code to apply.

        Returns:
            HttpResponseRedirect: The HTTP redirect response object.
        """
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
        """
        Processes the checkout and creates an order.

        Args:
            request (HttpRequest): The HTTP request object.
            form (OrderForm): The form object containing the order details.
            describe (str): The description of the order.
            table_number (str): The table number for the order.
            customer_name (str): The name of the customer.
            phone_number (str): The phone number of the customer.

        Returns:
            HttpResponseRedirect: The HTTP redirect response object.
        """
        self.load_data_from_cookie(request)
        session_data = request.session.get("order", {})
        order_dict = session_data.get("order", {})
        cart_items = Item.objects.filter(id__in=self.data.keys())
        values=(self.data.values())
        prices=self.calculate_price(self.data)
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
        return redirect('cafe:home')
    
    def calculate_price(self,item_quantity_dict):
        """
        Calculates the price for each item in the cart.

        Args:
            item_quantity_dict (dict): The dictionary containing item IDs and quantities.

        Returns:
            list: The list of prices for each item.
        """
        total_price = 0
        price_list=[]

        for item_id, quantity in item_quantity_dict.items():
            item = get_object_or_404(Item, id=item_id)
            item_price = item.price
            total_price = item_price * int(quantity)
            price_list.append(total_price)

        return price_list
    
    def calculate_total_price(self,item_quantity_dict):
        """
        Calculates the total price of the order.

        Args:
            item_quantity_dict (dict): The dictionary containing item IDs and quantities.

        Returns:
            float: The total price of the order.
        """
        total_price = 0

        for item_id, quantity in item_quantity_dict.items():
            item = get_object_or_404(Item, id=item_id)
            item_price = item.price
            total_price += item_price * int(quantity)

        return total_price
    
    def calculate_total_quantity(self , item_quantity_dict):
        """
        Calculates the total quantity of items in the cart.

        Args:
            item_quantity_dict (dict): The dictionary containing item IDs and quantities.

        Returns:
            int: The total quantity of items in the cart.
        """
        total_quantity=0

        for _, quantity in item_quantity_dict.items():
            total_quantity +=int(quantity)

        return total_quantity


class ViewCartView(View):
    """
    A class-based view for handling the view cart functionality.

    Attributes:
        template_name (str): The name of the template to render.
        data (dict): The data dictionary for storing cart items.

    Methods:
        load_data_from_cookie(request): Loads cart data from cookies.
        save_data_to_cookie(response): Saves cart data to cookies.
        save_data_to_session(request): Saves cart data to session.
        get(request): Handles GET requests.
        post(request, *args, **kwargs): Handles POST requests.
        save(item_id, quantity): Saves an item to the cart.
        calculate_price(item_quantity_dict): Calculates the price for each item in the cart.
    """
    template_name='orders/cart.html'
    data = {}

    def load_data_from_cookie(self, request):
        """
        Loads cart data from cookies.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            None
        """
        cart_cookie = request.COOKIES.get('cart', '{}')
        try:
            self.data = json.loads(cart_cookie)
        except json.JSONDecodeError:
            self.data = {}

    def save_data_to_cookie(self, response):
        """
        Saves cart data to cookies.

        Args:
            response (HttpResponse): The HTTP response object.

        Returns:
            None
        """
        expiration_date = datetime.now() + timedelta(days=365)
        response.set_cookie("cart", json.dumps(self.data), expires=expiration_date)

    def save_data_to_session(self, request):
        """
        Saves cart data to session.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            None
        """
        request.session['cart'] = self.data

    def get(self, request):
        """
        Handles GET requests.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The HTTP response object.
        """
        self.load_data_from_cookie(request)
        cart_form = CartAddForm()
        cart_items = Item.objects.filter(id__in=self.data.keys())
        cafe = get_object_or_404(Cafe)
        values=(self.data.values())
        prices=self.calculate_price(self.data)
        combined_items = zip_longest(cart_items, values, prices, fillvalue=None)

        return render(request, self.template_name, {'combined_items': combined_items,'cart_form':cart_form, "cafe":cafe})
    
    def post(self, request, *args, **kwargs):
        """
        Handles POST requests.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: The HTTP response object.
        """
        self.load_data_from_cookie(request)
        form = CartAddForm(request.POST)
        if form.is_valid():
            item_id = request.POST.get('item_id')
            quantity = request.POST.get('quantity')
            action = request.POST.get('action')
            print(action)
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
        """
        Saves an item to the cart.

        Args:
            item_id (str): The ID of the item to save.
            quantity (str): The quantity of the item.

        Returns:
            None
        """
        self.data[item_id] += int(quantity)
        order = {"id": generate_random_id(), "item": self.data}
        self.request.session["order"] = {"order": order, "status": ""}
        print(f"Saving item {item_id} with quantity {quantity}")
        
    def calculate_price(self,item_quantity_dict):
        """
        Calculates the price for each item in the cart.

        Args:
            item_quantity_dict (dict): The dictionary containing item IDs and quantities.

        Returns:
            list: The list of prices for each item.
        """
        total_price = 0
        price_list=[]

        for item_id, quantity in item_quantity_dict.items():
            item = get_object_or_404(Item, id=item_id)
            item_price = item.price
            total_price = item_price * int(quantity)
            price_list.append(total_price)

        return price_list

        







            

            


