#from django.shortcuts import render
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
# Create your views here.
from .models import *
from .serializers import *
from .permission import *


### Views de Ponentes con sus Permisos
class PonenteView(generics.ListAPIView):
  """ 
  vista para listar ponentes, todos los usuarios tanto registrados como no pueden acceder 
  """
  authentication_classes = (TokenAuthentication,)
  permission_classes = [IsLoggedInUserOrAnonymous]
  queryset = Ponente.objects.all()
  serializer_class = PonenteSerializer

class CreatePonenteView(generics.CreateAPIView):
  """ 
  vista para crear ponentes, el usuario administrador es el unico que puede crearlos
  """
  authentication_classes = (TokenAuthentication,)
  permission_classes = [IsAdminUser]
  #lookup_field = 'id'
  queryset = Ponente.objects.all()
  serializer_class = PonenteSerializer

class PonenteRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
  """ 
  vista para actualizar, eliminar y ver un ponente, el usuario administrador es el unico que puede acceder
  """
  authentication_classes = (TokenAuthentication,)
  permission_classes = [IsAdminUser]
  #lookup_field = 'id'
  queryset = Ponente.objects.all()
  serializer_class = PonenteSerializer
  
### Views de Ponencias con sus Permisos
class PonenciaView(generics.ListAPIView):
  """ 
  vista para listar ponencias, todos los usuarios tanto registrados como no pueden acceder 
  """
  authentication_classes = (TokenAuthentication,)
  permission_classes = [IsLoggedInUserOrAnonymous]
  queryset = Ponencia.objects.all()
  serializer_class = PonenciaSerializer

class CreatePonenciaView(generics.CreateAPIView):
  """ 
  vista para crear ponencias, el usuario administrador es el unico que puede crearlas
  """
  authentication_classes = (TokenAuthentication,)
  permission_classes = [IsAdminUser]
  queryset = Ponencia.objects.all()
  serializer_class = PonenciaSerializer

class PonenciaRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
  """ 
  vista para actualizar, eliminar y ver una ponencia, el usuario administrador es el unico que puede acceder
  """
  authentication_classes = (TokenAuthentication,)
  permission_classes = [IsAdminUser]
  #lookup_field = 'id'
  queryset = Ponencia.objects.all()
  serializer_class = PonenciaSerializer

  def put(self, request, *args, **kwargs):
    return self.partial_update(request, *args, **kwargs)

# def getPonenteById(request, param):
#   data = Ponente.objects.filter(id=param)
#   return JsonResponse(list(data.values("id","name","age")),safe=False)
