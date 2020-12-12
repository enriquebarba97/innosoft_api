from django.shortcuts import render
from .models import Asistencia
from .serializers import *
from rest_framework import generics


# Create your views here.

class AsistenciaView(generics.ListCreateAPIView):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer

class AsistenciaRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer


