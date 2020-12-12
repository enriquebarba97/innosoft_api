from django.urls import path
from .views import *

urlpatterns = [
    path("asistencias/", AsistenciaView.as_view(), name="asistencias_view"),
    path("asistencias/create", AsistenciaCreateView.as_view(), name="asistencias_create"),
    path("asistencias/check/<int:pk>", AsistenciaCheckView.as_view(), name="asistencias_check"),
    path("asistencias/<int:pk>", AsistenciaRetrieveDestroyView.as_view(), name="asistencias_retrieve_destroy"),
    path("asistencias/usuario/<int>", AsistenciaUsuarioView.as_view(), name="asistencias_por_usuario"),
    path("asistencias/ponencia/<int>", AsistenciaPonenciaView.as_view(), name="asistencias_por_ponencia")   
]
