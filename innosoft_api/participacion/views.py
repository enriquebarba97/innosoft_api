from .models import Asistencia
from participacion.serializers import *
from rest_framework import generics


# Create your views here.

class AsistenciaCreateView(generics.CreateAPIView):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaCreateSerializer

class AsistenciaRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer

class AsistenciaCheckView(generics.UpdateAPIView):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaCheckSerializer

class AsistenciaView(generics.ListAPIView):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer

class AsistenciaUsuarioView(generics.ListAPIView):
    serializer_class = AsistenciaSerializer

    def get_queryset(self):
        usuario = self.kwargs["int"]
        return Asistencia.objects.filter( usuario = usuario)

class AsistenciaPonenciaView(generics.ListAPIView):
    serializer_class = AsistenciaSerializer

    def get_queryset(self):
        ponencia = self.kwargs["int"]
        return Asistencia.objects.filter( ponencia = ponencia)


