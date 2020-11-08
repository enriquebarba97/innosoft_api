from django.urls import path
from . import views
urlpatterns = [
    path('', views.getPonentes),
    path('<int:param>/', views.getPonenteById)
]