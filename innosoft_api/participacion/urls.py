from django.urls import path
from .views import *

urlpatterns = [
    path("asistencias/", AsistenciaView.as_view(), name="asistencias_view"),
<<<<<<< HEAD
    path("asistencias/create", AsistenciaCreateView.as_view(), name="asistencias_create"),
    path("asistencias/check/<int:pk>", AsistenciaCheckView.as_view(), name="asistencias_check"),
    path("asistencias/<int:pk>", AsistenciaRetrieveDestroyView.as_view(), name="asistencias_retrieve_destroy")


=======
    path("asistencias/<int:pk>", AsistenciaRetrieveUpdateDelete.as_view(),name='asistencia_retrieve_update_delete'),
    path("asistencias/usuario/<int>", AsistenciaUsuarioView.as_view(), name="asistencias_por_usuario"),
    path("asistencias/ponencia/<int>", AsistenciaPonenciaView.as_view(), name="asistencias_por_ponencia")   
>>>>>>> 7bf7749f0bde5140cf8695a475ba51ce65197b00
]