from django.test import TestCase

# Create your tests here.

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from programa.models import Ponente

class PonenteTests(APITestCase):

    def setUp(self):
        """
        Preparamos la base de datos con un Ponente de prueba.
        """
        Ponente.objects.create(id="1", name="Ponente Base 1", surname="Surname Base 1", phone="123547896", email="base1@gmail.com")
        Ponente.objects.create(id="2", name="Ponente Base 2", surname="Surname Base 2", phone="854125478", email="base2@gmail.com")


    def test_crear_ponente(self):
        """
        Aseguramos que se puede crear una entidad Ponente.
        """
        url = reverse("ponentes_view")
        data = {"name": "Ponente Test 1", "surname": "Surname 1", "phone": "684362467", "email": "ponente1@gmail.com"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ponente.objects.filter(name="Ponente Test 1").count(), 1)
        self.assertEqual(Ponente.objects.filter(name="Ponente Test 1").get().id, 3)
        self.assertEqual(Ponente.objects.filter(id="3").get().name, "Ponente Test 1")
        self.assertEqual(Ponente.objects.filter(id="3").get().surname, "Surname 1")
        self.assertEqual(Ponente.objects.filter(id="3").get().phone, "684362467")
        self.assertEqual(Ponente.objects.filter(id="3").get().email, "ponente1@gmail.com")

    
    def test_obtener_ponente_por_id(self):
        """
        Aseguramos que se puede obtener un ponente por su id
        """
        url = reverse("ponente_retrieve_update_delete", kwargs={"pk":"1"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"id": 1, "name": "Ponente Base 1", "surname":"Surname Base 1" , "phone":"123547896" , "email":"base1@gmail.com" })

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

        self.assertEqual(first_result, {"id": 1, "name": "Ponente Base 1", "surname":"Surname Base 1" , "phone":"123547896" , "email":"base1@gmail.com" })
        self.assertEqual(second_result, {"id": 2, "name": "Ponente Base 2", "surname":"Surname Base 2" , "phone":"854125478" , "email":"base2@gmail.com" })
