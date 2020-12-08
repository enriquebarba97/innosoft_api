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




    def test_crear_ponente(self):
        """
        Aseguramos que se puede crear una entidad Ponente.
        """
        url = reverse("ponentes_view")
        data = {"name": "Ponente Test 1", "surname": "Surname 1", "phone": "684362467", "email": "ponente1@gmail.com"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ponente.objects.filter(name="Ponente Test 1").count(), 1)
        self.assertEqual(Ponente.objects.get().name, "Ponente Test 1")
        self.assertEqual(Ponente.objects.get().surname, "Surname 1")
        self.assertEqual(Ponente.objects.get().phone, "684362467")
        self.assertEqual(Ponente.objects.get().email, "ponente1@gmail.com")
