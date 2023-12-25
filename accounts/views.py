from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from .forms import UserLoginForm
from django.views import View
from .authenticate import PhoneBackend
from django.contrib.auth import login
import datetime
from  .models import User
# Create your views here.

    
class UserLoginView(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, "accounts/login.html", {"form":form})
            
    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = PhoneBackend.authenticate(request, username=cd["phone_number"], password=cd["password"])
            if user is not None:
                login(request, user, backend="django.contrib.auth.backends.ModelBackend")
                return render(request, "accounts/staff.html")
        return render(request, "accounts/login.html", {"form":form})



def Usercookiesview(request, user_id):

    user = user_id_func(user_id)
    request.session['recent_event_id'] = user.id
    request.session['recent_event_title'] = user.name

    response = HttpResponse("Event View")
    response.set_cookie('user_id', f"{user.id}")
    response.set_cookie('user.name' , f"{user.name}")


def user_id_func (user_id):
    try:
        event = User.objects.get(id=user_id)
        return event
    except User.DoesNotExist:
        raise Http404("Event does not exist")