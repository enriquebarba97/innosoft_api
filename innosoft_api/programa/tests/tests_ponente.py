from django.urls import reverse
from rest_framework import status
from registro.tests import BaseTestCase
from programa.models import Ponente

class PonenteTests(BaseTestCase):

    def setUp(self):
        """
        Preparamos la base de datos con un par de Ponentes de prueba.
        """
        Ponente.objects.create(name="Ponente Base 1", surname="Surname Base 1", phone="123547896", email="base1@gmail.com")
        Ponente.objects.create(name="Ponente Base 2", surname="Surname Base 2", phone="854125478", email="base2@gmail.com")
        super().setUp()


    #------------------------------------------------------------------------------------------------------ READ

    def test_obtener_ponente_por_id_sin_permisos(self):
            """
            Aseguramos que no se puede obtener un ponente por su id sin permisos
            """
            url = reverse("ponente_retrieve_update_delete", kwargs={"pk":"1"})
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_obtener_ponente_por_id_con_permisos(self):
            """
            Aseguramos que un admin puede obtener un ponente por su id
            """
            self.get_token()

            url = reverse("ponente_retrieve_update_delete", kwargs={"pk":"1"})
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            ponente = Ponente.objects.get(pk=1)

            self.assertEqual(response.data["id"], ponente.id)
            self.assertEqual(response.data["name"], ponente.name)
            self.assertEqual(response.data["surname"], ponente.surname)
            self.assertEqual(response.data["phone"], ponente.phone)
            self.assertEqual(response.data["email"], ponente.email)

            self.remove_token()


    def test_obtener_ponentes_sin_permisos(self):
        """
        Aseguramos que los usuarios anonimos pueden obtener todos los ponentes
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

    def test_obtener_ponentes_con_permisos(self):
        """
        Aseguramos que los usuarios logeados pueden obtener todos los ponentes
        """
        self.get_token(uvus = "participante")

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
               
        self.remove_token()

    #------------------------------------------------------------------------------------------------------ CREATE

    def test_crear_ponente_sin_permisos(self):
        """
        Aseguramos que no se puede crear una entidad Ponente sin permisos.
        """
        url = reverse("create_ponentes_view")

        test_name = "Ponente Test 1"
        test_surname = "Surname 1"
        test_phone = "684362467"
        test_email = "ponente1@gmail.com"

        data = {"name":test_name, "surname":test_surname, "phone":test_phone, "email":test_email}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Ponente.objects.filter(name=test_name).count(), 0)

    def test_crear_ponente_con_permisos(self):
        """
        Aseguramos que un admin puede crear una entidad Ponente.
        """
        self.get_token()

        url = reverse("create_ponentes_view")

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

        self.remove_token()

    #------------------------------------------------------------------------------------------------------ DELETE

    def test_borrar_ponente_sin_permisos(self):
        """
        Aseguramos que no se puede borrar un ponente sin permisos
        """
        url = reverse("ponente_retrieve_update_delete", kwargs={"pk":"1"})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Ponente.objects.filter(id="1").count(), 1)
        

    def test_borrar_ponente_con_permisos(self):
        """
        Aseguramos que un admin puede borrar un ponente
        """
        self.get_token()

        url = reverse("ponente_retrieve_update_delete", kwargs={"pk":"1"})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ponente.objects.filter(id="1").count(), 0)

        self.remove_token()

    #------------------------------------------------------------------------------------------------------ UPDATE

    def test_actualizar_ponente_sin_permisos(self):
        """
        Aseguramos que no se puede actualizar un ponente sin permisos
        """
        url = reverse("ponente_retrieve_update_delete", kwargs={"pk":"2"})
        data = {"name":"Updated Name 2"}
        response = self.client.put(url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        second_ponente = Ponente.objects.get(pk=2)

        self.assertEqual(second_ponente.name, "Ponente Base 2")

    def test_actualizar_ponente_con_permisos(self):
        """
        Aseguramos que un admin puede actualizar un ponente
        """
        self.get_token()

        url = reverse("ponente_retrieve_update_delete", kwargs={"pk":"2"})
        data = {"name":"Updated Name 2"}
        response = self.client.put(url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        second_ponente = Ponente.objects.get(pk=2)

        self.assertEqual(second_ponente.name, "Updated Name 2")

        self.remove_token()

    #==============================================================================================
    # Tests modelo

    def test_crear_ponente(self):
        """
        Aseguramos que se puede crear un ponente con datos correctos.
        """
        Ponente(name="Ponente", surname="Test", phone="123456789", email="ponentetest@gmail.com").save()
        
        self.assertEqual(Ponente.objects.all().count(), 3)

        ponente_test = Ponente.objects.get(pk=3)

        self.assertEqual(ponente_test.name, "Ponente")
        self.assertEqual(ponente_test.surname, "Test")
        self.assertEqual(ponente_test.phone, "123456789")
        self.assertEqual(ponente_test.email, "ponentetest@gmail.com")
