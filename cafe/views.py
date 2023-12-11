from django.shortcuts import render, get_object_or_404

# Create your views here.

def home(request):
    if request.method == "GET":
        return render(request, "", context={})


# def products(request):
#     if request.method == "GET":
#         return render(request, "", context={})
#     elif request.method == "POST":
#         pass
        


# def menu(request):
#     if request.method == "GET":
#         products = Product.all()
#         return render(request, "", context={"products":products})
    

def product_detail(request, slug):
    if request.method == "GET":
        product_detail = get_object_or_404(Product, slug=slug)
        return render(request, "", context={})
    
    
def about(request):
    if request == "GET":
        return render(request, context={})
    