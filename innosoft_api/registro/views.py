from .models import User
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.authentication import TokenAuthentication
from .permission import *
from .serializers import UserCreateSerializer,UpdateUserSerializer,ListUserSerializer
from rest_framework.viewsets import ViewSet
from .serializers import UploadSerializer
from rest_framework.response import Response
import pandas as pd
from django.contrib.auth.models import Group
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action

class ListUsersView(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = ListUserSerializer
class RegisterView(generics.CreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [AdminPass]
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
class UpdateDeleteUserView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [AdminPass]
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class FileUploadView(ViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [AdminPass]
    serializer_class = UploadSerializer
    @swagger_auto_schema(
        operation_description='Upload container excel, if the columns and data are valid.',
        manual_parameters=[openapi.Parameter(
                            name="file_uploaded",
                            in_=openapi.IN_FORM,
                            type=openapi.TYPE_FILE,
                            required=True,
                            description="Documento excel en formato xls con los usuarios a añadir a partir de la linea 8, siguiendo la plantilla aportada por el profesor."
                            )],
        responses={400: 'Invalid data in uploaded file',
                   200: 'Success'},
    )
    @action(detail=False, methods=['post'], parser_classes=(MultiPartParser, ), name='upload-excel')
    def upload_excel(self, request):
        file_uploaded = request.FILES.get('file_uploaded')
        if file_uploaded == None:
            return Response("No file provided", status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                tabla = pd.read_excel(file_uploaded.read())
                cont = 0
                cont2 = 0
                for row in tabla.iterrows():
                    cont+=1
                    if cont>6:
                        name = row[1][1].split(",")
                        if(User.objects.filter(uvus=row[1][2]).count()==0):
                            User.objects.create(uvus=row[1][2],first_name=name[1],last_name=name[0],email=row[1][4])
                            User.objects.get(uvus=row[1][2]).groups.set([Group.objects.get(pk=4)])
                            cont2+=1
                response = "You have uploaded {} new users".format(cont2)
                return Response(response)
            except:
                return Response("The file provided was not valid", status=status.HTTP_400_BAD_REQUEST)

        
