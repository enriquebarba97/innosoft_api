#from django.shortcuts import render
from rest_framework import generics
# Create your views here.
from .models import *
from .serializers import *

class PonenteView(generics.ListCreateAPIView):
  queryset = Ponente.objects.all()
  serializer_class = PonenteSerializer

class PonenteRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
  #lookup_field = 'id'
  queryset = Ponente.objects.all()
  serializer_class = PonenteSerializer
  

class PonenciaView(generics.ListCreateAPIView):
  queryset = Ponencia.objects.all()
  serializer_class = PonenciaSerializer

class PonenciaRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
  #lookup_field = 'id'
  queryset = Ponencia.objects.all()
  serializer_class = PonenciaSerializer

# def getPonenteById(request, param):
#   data = Ponente.objects.filter(id=param)
#   return JsonResponse(list(data.values("id","name","age")),safe=False)