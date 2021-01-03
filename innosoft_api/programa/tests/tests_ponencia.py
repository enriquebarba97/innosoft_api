from django.test import TestCase

# Create your tests here.

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from programa.models import Ponencia, Ponente
from registro.tests import BaseTestCase
import datetime

class PonenciaTests(BaseTestCase):

    #------------------------------------------------------------------------------------------------------READ

    def test_obtener_ponencias_sin_permisos(self):
        """
        Aseguramos que no se puedan obtener todas las ponencias
        """
        url = reverse("ponencia_view")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset({"count":2}, response.data)


        first_result = response.data["results"][0]
        first_ponencia = Ponencia.objects.get(pk=1)

        #Comprobamos los atributos básicos de Ponencia 1
        self.assertEqual(first_result["id"], first_ponencia.id)
        self.assertEqual(first_result["name"], first_ponencia.name)
        self.assertEqual(first_result["description"], first_ponencia.description)
        self.assertEqual(first_result["time"], first_ponencia.time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        self.assertEqual(first_result["place"], first_ponencia.place)

        #Comprobamos que la ponencia tiene los ponentes correspondientes
        self.assertEqual(len(first_result["ponentes"]), 2)

        #Comprobamos que los ponentes de la ponencia son correctos
        self.assertEqual(first_result["ponentes"][0]["id"], 1)
        self.assertEqual(first_result["ponentes"][0]["name"], Ponente.objects.get(pk=1).name)

        self.assertEqual(first_result["ponentes"][1]["id"], 2)
        self.assertEqual(first_result["ponentes"][1]["name"], Ponente.objects.get(pk=2).name)



        second_result = response.data["results"][1]
        second_ponencia = Ponencia.objects.get(pk=2)

        #Comprobamos los atributos básicos de Ponencia 2
        self.assertEqual(second_result["id"], second_ponencia.id)
        self.assertEqual(second_result["name"], second_ponencia.name)
        self.assertEqual(second_result["description"], second_ponencia.description)
        self.assertEqual(second_result["time"], second_ponencia.time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        self.assertEqual(second_result["place"], second_ponencia.place)

        #Comprobamos que la ponencia tiene los ponentes correspondientes
        self.assertEqual(len(second_result["ponentes"]), 1)

        #Comprobamos que el ponente de la ponencia es correcto
        self.assertEqual(second_result["ponentes"][0]["id"], 2)
        self.assertEqual(second_result["ponentes"][0]["name"], Ponente.objects.get(pk=2).name)

    def test_obtener_ponencia_por_id_sin_permisos(self):
        """
        Aseguramos que se puede obtener una ponencia por su id
        """
        url = reverse("ponencia_retrieve_update_delete", kwargs={"pk":"2"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ponencia = Ponencia.objects.get(pk=2)

        self.assertEqual(response.data["id"], ponencia.id)
        self.assertEqual(response.data["name"], ponencia.name)
        self.assertEqual(response.data["description"], ponencia.description)
        self.assertEqual(response.data["time"], ponencia.time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        self.assertEqual(response.data["place"], ponencia.place)

        self.assertEqual(len(response.data["ponentes"]), 1)

        self.assertEqual(response.data["ponentes"][0]["id"], 2)
        self.assertEqual(response.data["ponentes"][0]["name"], Ponente.objects.get(pk=2).name)

    def test_obtener_ponencia_por_id_con_permisos(self):
        """
        Aseguramos que se puede obtener una ponencia por su id
        """
        url = reverse("ponencia_retrieve_update_delete", kwargs={"pk":"2"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ponencia = Ponencia.objects.get(pk=2)

        self.assertEqual(response.data["id"], ponencia.id)
        self.assertEqual(response.data["name"], ponencia.name)
        self.assertEqual(response.data["description"], ponencia.description)
        self.assertEqual(response.data["time"], ponencia.time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        self.assertEqual(response.data["place"], ponencia.place)

        self.assertEqual(len(response.data["ponentes"]), 1)

        self.assertEqual(response.data["ponentes"][0]["id"], 2)
        self.assertEqual(response.data["ponentes"][0]["name"], Ponente.objects.get(pk=2).name)

    #------------------------------------------------------------------------------------------------------ CREATE   

    def test_crear_ponencia_sin_permisos(self):
        """
        Aseguramos que se puede crear una entidad Ponencia.
        """
        url = reverse("ponencia_view")

        test_name = "Ponencia Test 1"
        test_description = "Descripcion Test 1"
        test_place = "Place Test 1"
        test_time = "2050-12-29T12:50"
        test_ponentes = ["1", "2"]

        data = {"name": test_name, "description":test_description, "place":test_place, "time":test_time, "ponentes":test_ponentes}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Ponencia.objects.filter(name=test_name).count(), 1)
        self.assertEqual(Ponencia.objects.filter(name=test_name).get().id, 3)
        self.assertEqual(Ponencia.objects.get(pk=3).name, test_name)
        self.assertEqual(Ponencia.objects.get(pk=3).description, test_description)
        self.assertEqual(Ponencia.objects.get(pk=3).place, test_place)
        self.assertEqual(Ponencia.objects.get(pk=3).time.strftime("%Y-%m-%dT%H:%M"), test_time)

        self.assertEqual(Ponencia.objects.get(pk=3).ponentes.count(), 2)

        self.assertEqual(Ponencia.objects.get(pk=3).ponentes.first(), Ponente.objects.get(pk=1))
        self.assertEqual(Ponencia.objects.get(pk=3).ponentes.last(), Ponente.objects.get(pk=2))



    def test_crear_ponencia_con_permisos(self):
        """
        Aseguramos que se puede crear una entidad Ponencia.
        """
        BaseTestCase.get_token(uvus = "admin")

        url = reverse("create_ponencia_view")

        test_name = "Ponencia Test 1"
        test_description = "Descripcion Test 1"
        test_place = "Place Test 1"
        test_time = "2050-12-29T12:50"
        test_ponentes = ["1", "2"]

        data = {"name": test_name, "description":test_description, "place":test_place, "time":test_time, "ponentes":test_ponentes}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Ponencia.objects.filter(name=test_name).count(), 1)
        self.assertEqual(Ponencia.objects.filter(name=test_name).get().id, 3)
        self.assertEqual(Ponencia.objects.get(pk=3).name, test_name)
        self.assertEqual(Ponencia.objects.get(pk=3).description, test_description)
        self.assertEqual(Ponencia.objects.get(pk=3).place, test_place)
        self.assertEqual(Ponencia.objects.get(pk=3).time.strftime("%Y-%m-%dT%H:%M"), test_time)

        self.assertEqual(Ponencia.objects.get(pk=3).ponentes.count(), 2)

        self.assertEqual(Ponencia.objects.get(pk=3).ponentes.first(), Ponente.objects.get(pk=1))
        self.assertEqual(Ponencia.objects.get(pk=3).ponentes.last(), Ponente.objects.get(pk=2))

        BaseTestCase.remove_token(uvus="admin")


    #------------------------------------------------------------------------------------------------------ DELETE

    def test_borrar_ponencia_sin_permisos(self):
        """
        Aseguramos que se puede borrar una Ponencia
        """
        url = reverse("ponencia_retrieve_update_delete", kwargs={"pk":"1"})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ponencia.objects.filter(id="1").count(), 0)

    def test_borrar_ponencia_con_permisos(self):
        """
        Aseguramos que se puede borrar una Ponencia
        """
        url = reverse("ponencia_retrieve_update_delete", kwargs={"pk":"1"})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ponencia.objects.filter(id="1").count(), 0)

    #------------------------------------------------------------------------------------------------------ UPDATE

    def test_actualizar_ponencia_sin_permisos(self):
        """
        Aseguramos que se puede actualizar una ponencia
        """
        url = reverse("ponencia_retrieve_update_delete", kwargs={"pk":"2"})

        updated_name = "Updated Ponencia Name 2"

        data = {"name":updated_name}
        response = self.client.put(url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        ponencia = Ponencia.objects.get(pk=2)

        self.assertEqual(ponencia.name, "Ponencia Base 2")

    def test_actualizar_ponencia_con_permisos(self):
        """
        Aseguramos que se puede actualizar una ponencia
        """
        url = reverse("ponencia_retrieve_update_delete", kwargs={"pk":"2"})

        updated_name = "Updated Ponencia Name 2"

        data = {"name":updated_name}
        response = self.client.put(url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        ponencia = Ponencia.objects.get(pk=2)

        self.assertEqual(ponencia.name, "Ponencia Base 2")