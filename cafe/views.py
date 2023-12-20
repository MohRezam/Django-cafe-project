from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Item
from django.views import View
# Create your views here.


class HomeView(View):
    def get(self, request):
        all_categories = Category.objects.all()        
        return render(request, "cafe/index.html", context={"all_categories":all_categories})

class CafeMenuView(View):
    def get(self, request, category_name):
        if category_name not in ["maincourse", "breakfast", "sweets", "cafe"]:
            return redirect("home")
        items = Item.objects.filter(category=category_name)
        return render(request, "cafe/menu-item.html", context={"items":items})
        
        


    