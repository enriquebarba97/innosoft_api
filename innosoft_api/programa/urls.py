from django.urls import path
from .views import *

urlpatterns = [
    path('ponentes/', PonenteView.as_view(), name='ponentes_view'),
    path('ponentes/create', CreatePonenteView.as_view(), name='create_ponentes_view'),
    path('ponentes/<int:pk>', PonenteRetrieveUpdateDelete.as_view(),name='ponente_retrieve_update_delete'),
    path('ponencias/', PonenciaView.as_view(), name='ponencia_view'),
    path('ponencias/create', CreatePonenciaView.as_view(), name='create_ponencia_view'),
    path('ponencias/<int:pk>', PonenciaRetrieveUpdateDelete.as_view(),name='ponencia_retrieve_update_delete'),
]