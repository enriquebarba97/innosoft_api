from django.urls import reverse
from rest_framework import status
from programa.models import Ponencia, Ponente
from registro.tests import BaseTestCase
from django.utils.timezone import make_aware
import datetime

class PonenciaTests(BaseTestCase):

    def setUp(self):
        """
        Preparamos la base de datos con un par de Ponencias de prueba.
        """
        Ponente.objects.create(name="Ponente Base 1", surname="Surname Base 1", phone="123547896", email="base1@gmail.com")
        Ponente.objects.create(name="Ponente Base 2", surname="Surname Base 2", phone="854125478", email="base2@gmail.com")

        Ponencia.objects.create(name="Ponencia Base 1", description="Descripción Base 1", time=make_aware(datetime.datetime.now()+datetime.timedelta(hours=5)), place="Sitio Base 1")
        Ponencia.objects.get(pk=1).ponentes.set([Ponente.objects.get(pk=1), Ponente.objects.get(pk=2)])

        Ponencia.objects.create(name="Ponencia Base 2", description="Descripción Base 2", time=make_aware(datetime.datetime.now()+datetime.timedelta(hours=5)), place="Sitio Base 2")
        Ponencia.objects.get(pk=2).ponentes.set([Ponente.objects.get(pk=2)])      
        super().setUp()


    #------------------------------------------------------------------------------------------------------READ

    def test_obtener_ponencias_sin_permisos(self):
        """
        Aseguramos que los usuarios anonimos puedan obtener todas las ponencias
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

    def test_obtener_ponencias_con_permisos(self):
        """
        Aseguramos que los usuarios logeados puedan obtener todas las ponencias
        """
        self.get_token(uvus="participante")

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

        self.remove_token()

    def test_obtener_ponencia_por_id_sin_permisos(self):
        """
        Aseguramos que no se puede obtener una ponencia por su id sin permisos
        """
        url = reverse("ponencia_retrieve_update_delete", kwargs={"pk":"2"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_obtener_ponencia_por_id_con_permisos(self):
        """
        Aseguramos que un admin puede obtener una ponencia por su id
        """
        self.get_token()

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

        self.remove_token()

    #------------------------------------------------------------------------------------------------------ CREATE   

    def test_crear_ponencia_sin_permisos(self):
        """
        Aseguramos que no se puede crear una entidad Ponencia sin permisos.
        """
        url = reverse("create_ponencia_view")

        test_name = "Ponencia Test 1"
        test_description = "Descripcion Test 1"
        test_place = "Place Test 1"
        test_time = "2050-12-29T12:50"
        test_ponentes = ["1", "2"]

        data = {"name": test_name, "description":test_description, "place":test_place, "time":test_time, "ponentes":test_ponentes}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertEqual(Ponencia.objects.filter(name=test_name).count(), 0)

    def test_crear_ponencia_con_permisos(self):
        """
        Aseguramos que un admin puede crear una entidad Ponencia.
        """
        self.get_token()

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

        self.remove_token()

    #------------------------------------------------------------------------------------------------------ DELETE

    def test_borrar_ponencia_sin_permisos(self):
        """
        Aseguramos que no se puede borrar una Ponencia sin permisos
        """
        url = reverse("ponencia_retrieve_update_delete", kwargs={"pk":"1"})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Ponencia.objects.filter(id="1").count(), 1)

    def test_borrar_ponencia_con_permisos(self):
        """
        Aseguramos que un admin puede borrar una Ponencia
        """
        self.get_token()

        url = reverse("ponencia_retrieve_update_delete", kwargs={"pk":"1"})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ponencia.objects.filter(id="1").count(), 0)

        self.remove_token()

    #------------------------------------------------------------------------------------------------------ UPDATE

    def test_actualizar_ponencia_sin_permisos(self):
        """
        Aseguramos que no se puede actualizar una ponencia sin permisos
        """
        url = reverse("ponencia_retrieve_update_delete", kwargs={"pk":"2"})

        updated_name = "Updated Ponencia Name 2"

        data = {"name":updated_name}
        response = self.client.put(url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        ponencia = Ponencia.objects.get(pk=2)

        self.assertEqual(ponencia.name, "Ponencia Base 2")

    def test_actualizar_ponencia_con_permisos(self):
        """
        Aseguramos que un admin puede actualizar una ponencia
        """
        self.get_token()
        # test_description = "Descripcion Test 1"
        # test_place = "Place Test 1"
        # test_time = "2050-12-29T12:50"
        # test_ponentes = ["1", "2"]

        url = reverse("ponencia_retrieve_update_delete", kwargs={"pk":"2"})
        # data = {"name": "Updated Name 2", "description":test_description, "place":test_place, "time":test_time, "ponentes":test_ponentes}
        data = {"name": "Updated Name 2"}
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
        ponencia = Ponencia.objects.get(pk=2)

        self.assertEqual(ponencia.name, "Updated Name 2")

        self.remove_token()