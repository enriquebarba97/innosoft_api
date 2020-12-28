from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import Group
from .models import User


class BaseTestCase(APITestCase):
    def setUp(self):
        GROUPS = ['administrador','moderador','staff','participante']
        self.client = APIClient()
        self.token = None

        for group in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group)
        user_administrador = User(uvus="admin",email="",first_name="admin",last_name="requeteadmin")
        user_administrador.set_password('qwerty')
        user_administrador.save()
        user_administrador.groups.add(Group.objects.get(name="administrador"))
        
        user_moderador = User(uvus="moder",email="",first_name="moderador",last_name="moderado")
        user_moderador.set_password('qwerty')
        user_moderador.save()
        user_moderador.groups.add(Group.objects.get(name="moderador"))

        user_staff = User(uvus="staff",email="",first_name="staff",last_name="staffado")
        user_staff.set_password('qwerty')
        user_staff.save()
        user_staff.groups.add(Group.objects.get(name="staff"))

        user_participante = User(uvus="participante",email="",first_name="participante",last_name="participio")
        user_participante.set_password('qwerty')
        user_participante.save()
        user_participante.groups.add(Group.objects.get(name="participante"))

    def tearDown(self):
        self.client = None
        self.token = None
    
    def get_token(self, uvus='admin', password='qwerty'):
        data = {'uvus': uvus, 'password': password}
        url = "/registro/auth/token/login"
        response = self.client.post(path=url,data=data)
        self.assertEqual(response.status_code, 200)
        self.token = response.json()['auth_token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def remove_token(self):
        self.client.credentials()
        self.token = None

class RegistroTests(BaseTestCase):

    def setUp(self):
        super().setUp()
        alum1 = User(uvus="testalum1",email="",first_name="alum1",last_name="alum1")
        alum1.set_password('qwerty')
        alum1.save()
        alum1.groups.add(Group.objects.get(name="participante"))

        alum2 = User(uvus="testalum2",email="",first_name="alum2",last_name="alum2")
        alum2.set_password('qwerty')
        alum2.save()
        alum2.groups.add(Group.objects.get(name="participante"))

        alum3 = User(uvus="testalum3",email="",first_name="alum3",last_name="alum3")
        alum3.set_password('qwerty')
        alum3.save()
        alum3.groups.add(Group.objects.get(name="participante"))

    def test_ver_alumnos(self):
        url = reverse('list_users')

        self.get_token(uvus="participante")
        response = self.client.get(url)
        self.assertEqual(response.status_code,403)
        self.remove_token()

        self.get_token()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.remove_token()