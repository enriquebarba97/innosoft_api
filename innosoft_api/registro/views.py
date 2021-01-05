from .models import User
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.authentication import TokenAuthentication
from .permission import *
from .serializers import UserCreateSerializer,UpdateUserSerializer,ListUserSerializer
from rest_framework.viewsets import ViewSet
from .serializers import UploadSerializer
from rest_framework.response import Response
import pandas as pd
from django.core.files.base import ContentFile
from django.contrib.auth.models import Group

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

class FileUploadView(ViewSet):
    serializer_class = UploadSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):
        file_uploaded = request.FILES.get('file_uploaded')
        content_type = file_uploaded.content_type
        tabla = pd.read_excel(file_uploaded.read())
        cont = 0
        for row in tabla.iterrows():
            cont+=1
            if cont>6:
                name = row[1][1].split(",")
                User.objects.create(uvus=row[1][2],first_name=name[1],last_name=name[0],email=row[1][4])
                User.objects.get(uvus=row[1][2]).groups.set([Group.objects.get(pk=4)])
        response = "POST API and you have uploaded a {} file".format(content_type)
        return Response(response)