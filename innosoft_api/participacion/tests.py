from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from participacion.models import Asistencia
from registro.models import User
from programa.models import Ponencia, Ponente
from django.contrib.auth.models import Group
from registro.tests import BaseTestCase
from django.utils.timezone import make_aware
from .qr_base64 import qr_in_base64
import datetime

class AsistenciaTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        User.objects.create(uvus="migueluvus", email="miguel@email.com",first_name="miguel",last_name="lastName1")
        User.objects.get(uvus="migueluvus").groups.set([Group.objects.get(name="participante")])

        Ponente.objects.create(name="Cote")
        Ponencia.objects.create(name="IA", description="Ponencia de IA", time=make_aware(datetime.datetime.now()+datetime.timedelta(hours=5)), place="Place1", categoria="IA")
        Ponencia.objects.get(pk=1).ponentes.set([Ponente.objects.get(pk=1)])

        User.objects.create(uvus="moisesuvus", email="moises@email.com",first_name="moises",last_name="lastName3")
        User.objects.get(uvus="moisesuvus").groups.set([Group.objects.get(name="participante")])

        User.objects.create(uvus="adriuvus", email="adri@email.com",first_name="adri",last_name="lastName2")
        User.objects.get(uvus="adriuvus").groups.set([Group.objects.get(name="participante")])

        Ponente.objects.create(name="Moises")
        Ponencia.objects.create(name="IA3", description="Ponencia de IA 3", time=make_aware(datetime.datetime.now()+datetime.timedelta(hours=5)), place="Place1", categoria="IA")
        Ponencia.objects.get(pk=2).ponentes.set([Ponente.objects.get(pk=2)])
        Ponencia.objects.create(name="IA3", description="Ponencia de IA 3", time=make_aware(datetime.datetime.now()+datetime.timedelta(hours=5)), place="Place1", categoria="IA")
        Ponencia.objects.get(pk=3).ponentes.set([Ponente.objects.get(pk=2)])

        Asistencia.objects.create(usuario=User.objects.get(pk=2), ponencia=Ponencia.objects.get(pk=2))
        Asistencia.objects.create(usuario=User.objects.get(pk=2), ponencia=Ponencia.objects.get(pk=3))
        Asistencia.objects.create(usuario=User.objects.get(pk=1), ponencia=Ponencia.objects.get(pk=3))
        Asistencia.objects.create(usuario=User.objects.get(uvus="participante"), ponencia=Ponencia.objects.get(pk=3))
        Asistencia.objects.create(usuario=User.objects.get(uvus="participante"), ponencia=Ponencia.objects.get(pk=2))

    def test_crear_asistencia_con_permisos_validos(self):
        BaseTestCase.get_token(self, uvus="participante")
        url = reverse("asistencias_create")

        test_usuario=User.objects.get(uvus="participante").id
        test_ponencia='1'
        data = {"usuario":test_usuario, "ponencia":test_ponencia}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Asistencia.objects.filter(usuario=test_usuario).count(), 3)
        self.assertEqual(Asistencia.objects.filter(usuario=test_usuario).filter(ponencia=test_ponencia).get().id, 6)
        self.assertEqual(Asistencia.objects.filter(ponencia=test_ponencia).count(), 1)
        self.assertEqual(Asistencia.objects.get(pk=2).asiste, False)
        BaseTestCase.remove_token(self)

    def test_crear_asistencia_sin_permisos(self):
        url = reverse("asistencias_create")

        test_usuario='1'
        test_ponencia='1'
        data = {"usuario":test_usuario, "ponencia":test_ponencia}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Asistencia.objects.filter(usuario=1).count(), 1)

    def test_obtener_asistencia_con_permisos(self):
        url = reverse("asistencias_retrieve_destroy", kwargs={"pk":"1"})
        BaseTestCase.get_token(self, uvus="admin")
        response = self.client.get(url)
        asistencia = Asistencia.objects.get(pk=1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Asistencia.objects.filter(usuario=1).count(), 1)
        self.assertEqual(response.data["id"], asistencia.id)
        self.assertEqual(response.data["usuario"], asistencia.usuario.id)
        self.assertEqual(response.data["ponencia"], asistencia.ponencia.id)
        self.assertEqual(response.data["asiste"], asistencia.asiste)
        BaseTestCase.remove_token(self)

    def test_obtener_asistencia_sin_permisos(self):
        url = reverse("asistencias_retrieve_destroy", kwargs={"pk":"1"})
        BaseTestCase.get_token(self, uvus="participante")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        BaseTestCase.remove_token(self)

    def test_obtener_asistencia_con_permisos_invalidos(self):
        url = reverse("asistencias_retrieve_destroy", kwargs={"pk":"2"})
        BaseTestCase.get_token(self, uvus="participante")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        BaseTestCase.remove_token(self)

    def test_borrar_asistencia_con_permisos_validos(self):
        url = reverse("asistencias_retrieve_destroy", kwargs={"pk":"1"})
        BaseTestCase.get_token(self, uvus="admin")
        response = self.client.delete(url)
        test_usuario='1'
        test_ponencia='1'
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Asistencia.objects.filter(usuario=test_usuario).count(), 1)
        self.assertEqual(Asistencia.objects.filter(ponencia=test_ponencia).count(), 0)
        BaseTestCase.remove_token(self)

    def test_borrar_asistencia_sin_permisos(self):
        url = reverse("asistencias_retrieve_destroy", kwargs={"pk":"1"})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_obtener_todas_asistencias_con_permisos_invalidos(self):
        url = reverse("asistencias_view")
        BaseTestCase.get_token(self, uvus="participante")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        BaseTestCase.remove_token(self)

    def test_obtener_todas_asistencias_con_permisos_validos(self):
        url = reverse("asistencias_view")
        BaseTestCase.get_token(self, uvus="staff")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset({"count":5}, response.data)


        first_result = response.data["results"][0]
        first_asistencia = Asistencia.objects.get(pk=1)

        self.assertEqual(first_result["id"], first_asistencia.id)
        self.assertEqual(first_result["usuario"], first_asistencia.usuario.id)
        self.assertEqual(first_result["ponencia"], first_asistencia.ponencia.id)
        self.assertEqual(first_result["asiste"], first_asistencia.asiste)

        second_result = response.data["results"][1]
        second_asistencia = Asistencia.objects.get(pk=2)

        self.assertEqual(second_result["id"], second_asistencia.id)
        self.assertEqual(second_result["usuario"], second_asistencia.usuario.id)
        self.assertEqual(second_result["ponencia"], second_asistencia.ponencia.id)
        self.assertEqual(second_result["asiste"], second_asistencia.asiste)

        third_result = response.data["results"][2]
        third_asistencia = Asistencia.objects.get(pk=3)

        self.assertEqual(third_result["id"], third_asistencia.id)
        self.assertEqual(third_result["usuario"], third_asistencia.usuario.id)
        self.assertEqual(third_result["ponencia"], third_asistencia.ponencia.id)
        self.assertEqual(third_result["asiste"], third_asistencia.asiste)
        BaseTestCase.remove_token(self)

    def test_obtener_todas_asistencias_sin_permisos(self):
        url = reverse("asistencias_view")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_obtener_asistencias_usuario_con_permisos(self):
        url = reverse("asistencias_por_usuario")
        BaseTestCase.get_token(self, uvus="participante")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset({"count":2}, response.data)


        first_result = response.data["results"][0]
        first_asistencia = Asistencia.objects.get(pk=4)

        self.assertEqual(first_result["id"], first_asistencia.id)
        self.assertEqual(first_result["usuario"], first_asistencia.usuario.id)
        self.assertEqual(first_result["ponencia"], first_asistencia.ponencia.id)
        self.assertEqual(first_result["asiste"], first_asistencia.asiste)

        second_result = response.data["results"][1]
        second_asistencia = Asistencia.objects.get(pk=5)

        self.assertEqual(second_result["id"], second_asistencia.id)
        self.assertEqual(second_result["usuario"], second_asistencia.usuario.id)
        self.assertEqual(second_result["ponencia"], second_asistencia.ponencia.id)
        self.assertEqual(second_result["asiste"], second_asistencia.asiste)
        BaseTestCase.remove_token(self)

    def test_obtener_asistencias_usuario_sin_permisos(self):
        url = reverse("asistencias_por_usuario")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_obtener_asistencias_ponencia_con_permisos_invalidos(self):
        url = reverse("asistencias_por_ponencia", kwargs={"int":"3"})
        BaseTestCase.get_token(self, uvus="participante")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        BaseTestCase.remove_token(self)

    def test_obtener_asistencias_ponencia_con_permisos_validos(self):
        url = reverse("asistencias_por_ponencia", kwargs={"int":"3"})
        BaseTestCase.get_token(self, uvus="staff")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset({"count":3}, response.data)


        first_result = response.data["results"][0]
        first_asistencia = Asistencia.objects.get(pk=2)

        self.assertEqual(first_result["id"], first_asistencia.id)
        self.assertEqual(first_result["usuario"], first_asistencia.usuario.id)
        self.assertEqual(first_result["ponencia"], first_asistencia.ponencia.id)
        self.assertEqual(first_result["asiste"], first_asistencia.asiste)

        second_result = response.data["results"][1]
        second_asistencia = Asistencia.objects.get(pk=3)

        self.assertEqual(second_result["id"], second_asistencia.id)
        self.assertEqual(second_result["usuario"], second_asistencia.usuario.id)
        self.assertEqual(second_result["ponencia"], second_asistencia.ponencia.id)
        self.assertEqual(second_result["asiste"], second_asistencia.asiste)
        BaseTestCase.remove_token(self)

    def test_obtener_asistencias_ponencias_sin_permisos(self):
        url = reverse("asistencias_por_ponencia", kwargs={"int":"3"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_qr_con_permisos(self):
        url = reverse("qr_de_asistencia", kwargs={"pk":"1"})
        BaseTestCase.get_token(self, uvus="participante")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["qr"], qr_in_base64(Asistencia.objects.get(pk=1).code))
        BaseTestCase.remove_token(self)

    def test_get_qr_sin_asistencia_con_permisos(self):
        url = reverse("qr_de_asistencia", kwargs={"pk":"99"})
        BaseTestCase.get_token(self, uvus="participante")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        BaseTestCase.remove_token(self)

    def test_get_qr_asistencia_sin_permisos(self):
        url = reverse("qr_de_asistencia", kwargs={"pk":"1"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_check_qr_con_permisos_invalidos(self):
        url = reverse("asistencias_qr_check")
        BaseTestCase.get_token(self, uvus="participante")
        Asistencia.objects.get(pk=1).asiste = False
        data = {"code":Asistencia.objects.get(pk=1).code, "ponenciaId":2}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        BaseTestCase.remove_token(self)

    def test_check_qr_con_permisos_validos(self):
        url = reverse("asistencias_qr_check")
        BaseTestCase.get_token(self, uvus="staff")
        Asistencia.objects.get(pk=1).asiste = False
        data = {"code":Asistencia.objects.get(pk=1).code, "ponenciaId":2}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Asistencia.objects.get(pk=1).asiste, True)
        BaseTestCase.remove_token(self)

    def test_check_qr_asiste_true_con_permisos_validos(self):
        url = reverse("asistencias_qr_check")
        BaseTestCase.get_token(self, uvus="staff")
        Asistencia.objects.get(pk=1).asiste = True
        data = {"code":Asistencia.objects.get(pk=1).code, "ponenciaId":2}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Asistencia.objects.get(pk=1).asiste, True)
        BaseTestCase.remove_token(self)

    def test_check_qr_sin_code_con_permisos_validos(self):
        url = reverse("asistencias_qr_check")
        BaseTestCase.get_token(self, uvus="staff")
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        BaseTestCase.remove_token(self)

    def test_check_asistencias_ponencia_sin_permisos(self):
        url = reverse("asistencias_qr_check")
        data = {"code":Asistencia.objects.get(pk=1).code, "ponenciaId":2}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
