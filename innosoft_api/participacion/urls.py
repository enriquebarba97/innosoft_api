from django.urls import path
from .views import *

urlpatterns = [
    path("asistencias/", AsistenciaView.as_view(), name="asistencias_view"),
    path("asistencias/<int:pk>", AsistenciaRetrieveUpdateDelete.as_view(),name='asistencia_retrieve_update_delete'),
    path("asistencias/usuario/<int>", AsistenciaUsuarioView.as_view(), name="asistencias_por_usuario"),
    path("asistencias/ponencia/<int>", AsistenciaPonenciaView.as_view(), name="asistencias_por_ponencia")   
]