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

    def test_ver_alumnos_permiso(self):
        url = reverse('list_users')

        self.get_token()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.remove_token()
        self.assertDictContainsSubset({"count":7}, response.data)

        response_5 = response.data["results"][4]
        response_6 = response.data["results"][5]

        test_alum_5 = User.objects.get(pk=5)
        test_alum_6 = User.objects.get(pk=6)

        self.assertEqual(response_5["uvus"], test_alum_5.uvus)
        self.assertEqual(response_5["first_name"], test_alum_5.first_name)
        self.assertEqual(response_5["last_name"], test_alum_5.last_name)

        self.assertEqual(response_6["uvus"], test_alum_6.uvus)
        self.assertEqual(response_6["first_name"], test_alum_6.first_name)
        self.assertEqual(response_6["last_name"], test_alum_6.last_name)

    
    def test_ver_alumnos_sinpermiso(self):
        url = reverse('list_users')

        self.get_token(uvus="participante")
        response = self.client.get(url)
        self.assertEqual(response.status_code,403)
        self.remove_token()

    def test_create_alumno_permiso(self):
        """
        Test para crear un usuario siendo un usuario registrado administrador
        """
        self.get_token()
        url = reverse('auth_register')
        data = {
    "uvus": "enrbarroq",
    "email": "enrbarroq@mod.es",
    "first_name": "Enrique",
    "last_name": "Barba",
    "password": "qwerty",
    "groups": [1]
}
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.get(uvus="enrbarroq").last_name,"Barba")
        self.remove_token()

    def test_create_alumno_sinpermiso(self):
        """
        Test para crear un usuario siendo un usuario sin permisos de edicion
        """
        url = reverse('auth_register')
        data = {
    "uvus": "enrbarroq",
    "email": "enrbarroq@mod.es",
    "first_name": "Enrique",
    "last_name": "Barba",
    "password": "qwerty",
    "groups": [
        1
    ]
}
        self.get_token(uvus="participante")
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 403)
        self.remove_token()

        self.get_token(uvus="moder")
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 403)
        self.remove_token()

        self.get_token(uvus="staff")
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 403)
        self.remove_token()

### Test Update and Show ####
    def test_update_alumno_permiso(self):
        """
        Test para actualizar un usuario siendo un usuario registrado administrador
        """
        self.get_token()
        url = reverse('update_delete_users', args=[3])
        data = {
    "id": "3",
    "uvus": "antferman2",
    "email": "moderador32@mod.es",
    "first_name": "modsurn4",
    "last_name": "prueba3",
    "groups": []
}
        response = self.client.put(url, data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.get(uvus="antferman2").last_name,"prueba3")
        self.remove_token()
    def test_update_alumno_sinpermiso(self):
        """
        Test para comprobar que no se puede actualizar un usuario siendo un participante
        """
        url = reverse('update_delete_users', args=[3])
        data = {
    "id": "3",
    "uvus": "antferman2",
    "email": "moderador32@mod.es",
    "first_name": "modsurn4",
    "last_name": "prueba3",
    "groups": [  
    ]
}
        self.get_token(uvus="participante")
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 403)
        self.remove_token()

        self.get_token(uvus="moder")
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 403)
        self.remove_token()

        self.get_token(uvus="staff")
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 403)
        self.remove_token()
        

    def test_ver_alumno_permiso(self):
        """
        Comprobar que deja acceso a show user siendo un usuario administrador
        """
        self.get_token()
        url = reverse('update_delete_users',kwargs={"pk":"3"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        usuario = User.objects.get(pk=3)
        self.assertEqual(response.data['uvus'],usuario.uvus)
        self.assertEqual(response.data['email'],usuario.email)
        self.assertEqual(response.data['first_name'],usuario.first_name)
        self.assertEqual(response.data['last_name'],usuario.last_name)
        self.remove_token()


    def test_ver_alumno_sinpermiso(self):
        """
        Ahora se comprueba que no se tiene acceso con un usuario alumno que es participante
        """
        self.get_token(uvus="participante")
        url = reverse('update_delete_users',kwargs={"pk":"3"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.remove_token()

    def test_delete_alumno_permiso(self):
        """
        Test para eliminar un usuario siendo administrador
        """
        self.get_token()
        url = reverse('update_delete_users',kwargs={"pk":"3"})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
    def test_delete_alumno_sinpermiso(self):
        """
        Test para eliminar un usuario siendo participante
        """
        self.get_token(uvus="participante")
        url = reverse('update_delete_users',kwargs={"pk":"3"})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)