from .models import Asistencia
from participacion.serializers import *
from rest_framework import generics, status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view


# Create your views here.

class AsistenciaCreateView(generics.CreateAPIView):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaCreateSerializer

class AsistenciaRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer

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

class AsistenciaQRView(generics.RetrieveAPIView):
    serializer_class = AsistenciaQRSerializer
    queryset = Asistencia.objects.all()

@api_view(['POST'])
def asistencia_qr_check(request):
    
    if "qr_b64" in request.data:
        qr_code = request.data["qr_b64"]

        try:
            instance =  Asistencia.objects.get(qr_b64=qr_code)
            if (instance.asiste == True):
                return Response("Se encontró la asistencia, pero ya está validada", status=status.HTTP_400_BAD_REQUEST)
            else:
                instance.asiste = True
                instance.save()
                return Response("Se validó la asistencia correctamente", status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response("No se encontró ninguna asistencia", status=status.HTTP_404_NOT_FOUND)

    else:
        return Response("No se aportó ningun QR", status=status.HTTP_400_BAD_REQUEST)