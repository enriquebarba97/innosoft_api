from django.test import TestCase

# Create your tests here.

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from programa.models import Ponente

class PonenteTests(APITestCase):

    def setUp(self):
        """
        Preparamos la base de datos con un par de Ponentes de prueba.
        """
        Ponente.objects.create(name="Ponente Base 1", surname="Surname Base 1", phone="123547896", email="base1@gmail.com")
        Ponente.objects.create(name="Ponente Base 2", surname="Surname Base 2", phone="854125478", email="base2@gmail.com")


    def test_crear_ponente(self):
        """
        Aseguramos que se puede crear una entidad Ponente.
        """
        url = reverse("ponentes_view")

        test_name = "Ponente Test 1"
        test_surname = "Surname 1"
        test_phone = "684362467"
        test_email = "ponente1@gmail.com"

        data = {"name":test_name, "surname":test_surname, "phone":test_phone, "email":test_email}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ponente.objects.filter(name=test_name).count(), 1)
        self.assertEqual(Ponente.objects.filter(name=test_name).get().id, 3)
        self.assertEqual(Ponente.objects.get(pk=3).name, test_name)
        self.assertEqual(Ponente.objects.get(pk=3).surname, test_surname)
        self.assertEqual(Ponente.objects.get(pk=3).phone, test_phone)
        self.assertEqual(Ponente.objects.get(pk=3).email, test_email)

    
    def test_obtener_ponente_por_id(self):
        """
        Aseguramos que se puede obtener un ponente por su id
        """
        url = reverse("ponente_retrieve_update_delete", kwargs={"pk":"1"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ponente = Ponente.objects.get(pk=1)

        self.assertEqual(response.data["id"], ponente.id)
        self.assertEqual(response.data["name"], ponente.name)
        self.assertEqual(response.data["surname"], ponente.surname)
        self.assertEqual(response.data["phone"], ponente.phone)
        self.assertEqual(response.data["email"], ponente.email)

    def test_obtener_ponentes(self):
        """
        Aseguramos que se pueden obtener todos los ponentes
        """
        url = reverse("ponentes_view")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset({"count":2}, response.data)

        first_result = response.data["results"][0]
        second_result = response.data["results"][1]

        first_ponente = Ponente.objects.get(pk=1)
        second_ponente = Ponente.objects.get(pk=2)

        self.assertEqual(first_result["id"], first_ponente.id)
        self.assertEqual(first_result["name"], first_ponente.name)
        self.assertEqual(first_result["surname"], first_ponente.surname)
        self.assertEqual(first_result["phone"], first_ponente.phone)
        self.assertEqual(first_result["email"], first_ponente.email)

        self.assertEqual(second_result["id"], second_ponente.id)
        self.assertEqual(second_result["name"], second_ponente.name)
        self.assertEqual(second_result["surname"], second_ponente.surname)
        self.assertEqual(second_result["phone"], second_ponente.phone)
        self.assertEqual(second_result["email"], second_ponente.email)

    def test_actualizar_ponente(self):
        """
        Aseguramos que se puede actualizar un ponente
        """
        url = reverse("ponente_retrieve_update_delete", kwargs={"pk":"2"})
        data = {"name":"Updated Name 2"}
        response = self.client.put(url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        second_ponente = Ponente.objects.get(pk=2)

        self.assertEqual(second_ponente.name, "Updated Name 2")

    def test_borrar_ponente(self):
        """
        Aseguramos que se puede borrar un ponente
        """
        url = reverse("ponente_retrieve_update_delete", kwargs={"pk":"1"})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ponente.objects.filter(id="1").count(), 0)
