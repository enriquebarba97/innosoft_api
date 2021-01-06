import os
from django.core.management.base import BaseCommand

#Sets up the system

class Command(BaseCommand):
    help = 'Sets up the system'

    def handle(self, *args, **kwargs):
        os.system("python .\innosoft_api\manage.py makemigrations registro")
        os.system("python .\innosoft_api\manage.py migrate registro")
        os.system("python .\innosoft_api\manage.py group")
        os.system("python .\innosoft_api\manage.py migrate")
        os.system("python .\innosoft_api\manage.py makemigrations programa")
        os.system("python .\innosoft_api\manage.py migrate programa")
        os.system("python .\innosoft_api\manage.py makemigrations participacion")
        os.system("python .\innosoft_api\manage.py migrate participacion")
        os.system("python .\innosoft_api\manage.py createAdmin")