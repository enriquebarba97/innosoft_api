from django.shortcuts import render
from .models import Asistencia
from .serializers import *
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


