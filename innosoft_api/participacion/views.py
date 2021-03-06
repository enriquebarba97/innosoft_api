from .models import Asistencia
from participacion.serializers import *
from rest_framework import generics, status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes, authentication_classes, schema
from .cryptography import decrypt
from .qr_base64 import qr_in_base64
import ast
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create your views here.

class AsistenciaCreateView(generics.CreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaCreateSerializer
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

class AsistenciaRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAdminUser]

    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer

class AsistenciaView(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAdminUser]

    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer

class AsistenciaUsuarioView(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    serializer_class = AsistenciaSerializer

    def get_queryset(self):
        usuario = self.request.user
        return Asistencia.objects.filter( usuario = usuario)

class AsistenciaPonenciaView(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAdminUser]
    serializer_class = AsistenciaSerializer

    def get_queryset(self):
        ponencia = self.kwargs["int"]
        return Asistencia.objects.filter( ponencia = ponencia)


@swagger_auto_schema(
                      method='post',
                      request_body=CodeSerializer,
                      responses={
                        200: "Se validó la asistencia correctamente",
                        400: "Se encontró la asistencia, pero ya está validada | No se aportó ningun QR | El código no pertenece a esa asistencia",
                        404: "No se encontró ninguna asistencia"
                      }
                    )
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def asistencia_qr_check(request):
  """
  Recibe el código que contiene el QR (b'...') y el id de la ponencia para validar la asistencia correspondiente
  """
  if ("code" in request.data and "ponenciaId" in request.data):
      encrypted_code = request.data["code"]
      ponencia_id = request.data["ponenciaId"]

      try:
          instance =  Asistencia.objects.get(code=encrypted_code)

          if (instance.ponencia.pk != ponencia_id):
              return Response("El código no pertenece a esa ponencia", status=status.HTTP_400_BAD_REQUEST)


          password = str(instance.usuario.id) + "" + str(instance.ponencia.id)

          decoded_code_bytes = decrypt(ast.literal_eval(encrypted_code), password)

          decoded_code = decoded_code_bytes.decode("utf-8")

          decoded_code = decoded_code.replace("X", "")

          values = decoded_code.split(" ")

          if (values[0] != "Usuario"+str(instance.usuario.id) or values[1] != "Ponencia"+str(instance.ponencia.id)):
              return Response("Validation error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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


@swagger_auto_schema(
                      method='get',
                      manual_parameters=[
                        openapi.Parameter('id', openapi.IN_QUERY, description="Id de la asistencia", type=openapi.TYPE_INTEGER)],
                      responses={
                        200: QRSerializer,
                        404: "No se encontró ninguna asistencia"
                      }
                    )
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def asistencia_qr(request, pk):
  """
  Devuelve la imagen QR (codificada en Base64) para verificar la asistencia
  """

  try:
      instance =  Asistencia.objects.get(pk = pk)

      response = {"qr":qr_in_base64(instance.code)}

      return Response(response, status=status.HTTP_200_OK)
  except ObjectDoesNotExist:
      return Response("No se encontró ninguna asistencia", status=status.HTTP_404_NOT_FOUND)

    
