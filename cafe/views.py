from django.shortcuts import render, get_object_or_404
from .models import Category, Item
# Create your views here.

def home(request):
    if request.method == "GET":
        all_categories = Category.objects.all()
        return render(request, "cafe/index.html", context={"all_categories": all_categories})



def cafe_menu(request, category_name):
    if request.method == "GET":
        # category = Category.objects.get(category_name=category_name)
        items = Item.objects.filter(category=category_name)
        
        return render(request, "cafe/menu-item.html", context={"items":items})


# def products(request):
#     if request.method == "GET":
#         return render(request, "", context={})
#     elif request.method == "POST":
#         pass
        


# def menu(request):
#     if request.method == "GET":
#         products = Product.all()
#         return render(request, "", context={"products":products})
    

# def product_detail(request, slug):
#     if request.method == "GET":
#         # product_detail = get_object_or_404(Product, slug=slug)
#         return render(request, "", context={})
    
    
# def about(request):
#     if request == "GET":
#         return render(request, context={})
    