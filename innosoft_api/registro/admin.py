from django.contrib import admin 
from django.utils.translation import ugettext_lazy as _ 
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin 
from django.contrib.auth import get_user_model 
from django.contrib.auth.admin import UserAdmin 
from django.contrib.auth.forms import UserChangeForm
from .models import User 
class UserAdmin(BaseUserAdmin): 
	form = UserChangeForm
	fieldsets = ( 
		(None, {'fields': ('uvus', 'email','password', )}), 
		(_('Personal info'), {'fields': ('first_name', 'last_name')}), 
		(_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 
										'groups', 'user_permissions')}), 
		(_('Important dates'), {'fields': ('last_login', 'date_joined')}), 
			
	) 
	add_fieldsets = ( 
		(None, { 
			'classes': ('wide', ), 
			'fields': ('email', 'password1', 'password2'), 
		}), 
	) 
	list_display = ['uvus', 'first_name', 'last_name', 'is_staff','email'] 
	search_fields = ('email', 'first_name', 'last_name','uvus') 
	ordering = ('uvus', ) 
admin.site.register(User, UserAdmin) 

