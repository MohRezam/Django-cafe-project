from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserForm, UserChangeForm
from django.contrib.auth.models import Group

# Register your models here.
class UserAdmin(BaseUserAdmin):
    """
    Custom UserAdmin class for managing User model in Django admin.
    """
    form = UserChangeForm
    add_form = UserForm
    
    list_display = ('email', 'phone_number', 'is_admin')
    list_filter = ('is_admin',)
    
    fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'full_name', 'password', 'address', 'national_id')}),
        ('Permissions', {'fields': ('is_active', 'is_admin','last_login')}),
    )

    add_fieldsets = (
        (None, {'fields':('phone_number', 'email', 'full_name', 'password1', 'password2', 'address', 'national_id')}),
    )
    search_fields = ('email', 'full_name')
    ordering = ('full_name',)
    filter_horizontal = ()
    
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
# admin.site.register(Customer)