from django.urls import path
from participacion.views import *

urlpatterns = [
    path("asistencias/", AsistenciaView.as_view(), name="asistencias_view"),
    path("asistencias/create", AsistenciaCreateView.as_view(), name="asistencias_create"),
    path("asistencias/<int:pk>", AsistenciaRetrieveDestroyView.as_view(), name="asistencias_retrieve_destroy"),
    path("asistencias/usuario", AsistenciaUsuarioView.as_view(), name="asistencias_por_usuario"),
    path("asistencias/ponencia/<int>", AsistenciaPonenciaView.as_view(), name="asistencias_por_ponencia"),

    path("asistencias/check", asistencia_qr_check, name="asistencias_qr_check"),
    path("asistencias/qr/<int:pk>", asistencia_qr, name="qr_de_asistencia")
    ]
