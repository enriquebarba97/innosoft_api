from .models import User
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from .permission import *
from .serializers import UserCreateSerializer,UpdateUserSerializer,ListUserSerializer

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