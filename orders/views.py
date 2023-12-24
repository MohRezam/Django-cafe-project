from django.shortcuts import render
from django.views import View
from .forms import UserSessionForm
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
    
