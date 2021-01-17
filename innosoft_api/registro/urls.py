from django.urls import path 
from rest_framework import routers
from django.conf.urls import include
from django.urls import include as inc
from .views import *

router = routers.DefaultRouter()
router.register(r'upload', FileUploadView, basename="upload")

urlpatterns = [ 
#path('auth/', include('djoser.urls')),
path('auth/', include('djoser.urls.authtoken')),
path('register/', RegisterView.as_view(), name='auth_register'),
path('register/users', ListUsersView.as_view(), name='list_users'),
path('register/users/<int:pk>', UpdateDeleteUserView.as_view(), name='update_delete_users'),
path('', inc(router.urls))
] 
