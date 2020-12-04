#from django.shortcuts import render
from rest_framework import generics
# Create your views here.
from .models import *
from .serializers import *
from .permissions import *

class PonenteView(generics.ListCreateAPIView):
  permission_classes = [HasGroupPermission]
  required_groups = {
         'GET': ['__all__'],
     }
  queryset = Ponente.objects.all()
  serializer_class = PonenteSerializer

class PonenteRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
  permission_classes = [HasGroupPermission]
  required_groups = {
         'GET': ['__all__'],
         'POST': ['administrador'],
         'PUT': ['administrador','moderador'],
         'DELETE': ['administrador'],
     }
  #lookup_field = 'id'
  queryset = Ponente.objects.all()
  serializer_class = PonenteSerializer
  

class PonenciaView(generics.ListCreateAPIView):
  permission_classes = [HasGroupPermission]
  required_groups = {
         'GET': ['__all__'],
     }
  queryset = Ponencia.objects.all()
  serializer_class = PonenciaSerializer

class PonenciaRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
  permission_classes = [HasGroupPermission]
  required_groups = {
         'GET': ['__all__'],
         'POST': ['administrador'],
         'PUT': ['administrador','moderador'],
         'DELETE': ['administrador'],
     }
  #lookup_field = 'id'
  queryset = Ponencia.objects.all()
  serializer_class = PonenciaSerializer

# def getPonenteById(request, param):
#   data = Ponente.objects.filter(id=param)
#   return JsonResponse(list(data.values("id","name","age")),safe=False)