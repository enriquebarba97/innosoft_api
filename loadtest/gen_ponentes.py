import json
import requests


HOST = "http://localhost:8000/"
UVUS = "admin"
PASS = "admin"
PHONE = "684362467"
EMAIL = "ponente1@gmail.com"


def create_ponentes(filename):
    """
    Create ponentes with requests library from ponentes.json
    """
    with open(filename) as f:
        ponentes = json.loads(f.read())

    data = {'uvus': UVUS , 'password': PASS}
    url = "registro/auth/token/login"
    response = requests.post(url=HOST+url,data=data)
    token = response.json()['auth_token']
    auth = {'Authorization': 'Token ' + token}
    for ponente in ponentes:
        data = {"name":ponente['name'], "surname":ponente['surname'], "phone":PHONE, "email":EMAIL}
        response = requests.post(HOST+"programa/ponentes/create", data ,headers=auth)

if __name__ == "__main__":
    create_ponentes('ponentes.json')
    print("Create ponentes success")