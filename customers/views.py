from django.shortcuts import render

# Create your views here.

def account(request):
    if request.method == "GET":
        return render(request, "", context={})
    
    
def bill(request):
    if request.method == "GET":
        return render(request, "", context={})
    