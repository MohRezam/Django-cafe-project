from django.shortcuts import render

# Create your views here.

def add_order(request):
    if request.method == "GET":
        return render(request, "", context={})
    
    
def checkout(request):
    if request.method == "GET":
        return render(request, "", context={})
    

def cart(request):
    if request.method == "GET":
        return render(request, "", context={})
    