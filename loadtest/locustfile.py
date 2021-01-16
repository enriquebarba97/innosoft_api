import json
import requests

from random import choice

from locust import (
    HttpUser,
    SequentialTaskSet,
    TaskSet,
    task,
    between
)


HOST = "http://localhost:8000/"

class DefVisualizer(TaskSet):


    @task
    def getPonencias(self):
        self.client.get("programa/ponencias/")
    
    @task
    def getPonentes(self):
        self.client.get("programa/ponentes/")

class DefShowPonente(SequentialTaskSet):

    def on_start(self):
        with open('ponentes.json') as f:
            self.ponentes = json.loads(f.read())
        self.ponente = choice(list(range(1,len(self.ponentes))))

    @task
    def authorization(self):
        data = {'uvus': 'admin', 'password': 'admin'}
        url = "registro/auth/token/login"
        response = self.client.post(url=url,data=data)
        token = response.json()['auth_token']
        self.auth = {'Authorization': 'Token ' + token}

    @task
    def getPonenteById(self):
        self.client.get("programa/ponentes/{0}".format(self.ponente),headers=self.auth)
    

class Visualizer(HttpUser):
    host = HOST
    tasks = [DefVisualizer]
    wait_time = between(3,5)

class ShowPonente(HttpUser):
    host = HOST
    tasks = [DefShowPonente]
    wait_time = between(3,5)