from django.shortcuts import render

# Create your views here.

def staffs(request):
    if request.method == "GET":
        return render(request, "", context={})
    
def manager(request):
    if request.method == "GET":
        return render(request, "", context={})
    