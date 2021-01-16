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


class Visualizer(HttpUser):
    host = HOST
    tasks = [DefVisualizer]
    wait_time = between(3,5)