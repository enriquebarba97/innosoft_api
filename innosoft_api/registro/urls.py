from django.contrib import admin 
from django.urls import path 
from django.conf.urls import include 
from .views import *
urlpatterns = [ 
#path('auth/', include('djoser.urls')),
path('auth/', include('djoser.urls.authtoken')),
path('register/', RegisterView.as_view(), name='auth_register'),
path('register/users', ListUsersView.as_view(), name='list_users'),
path('register/users/<int:pk>',UpdateDeleteUserView.as_view(), name='update_delete_users')
] 
