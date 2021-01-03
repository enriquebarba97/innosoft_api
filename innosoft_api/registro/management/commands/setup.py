import os

#Sets up the system

os.system("python .\innosoft_api\manage.py makemigrations registro")
os.system("python .\innosoft_api\manage.py migrate registro")
os.system("python .\innosoft_api\manage.py group")
os.system("python .\innosoft_api\manage.py migrate")
os.system("python .\innosoft_api\manage.py makemigrations programa")
os.system("python .\innosoft_api\manage.py migrate programa")
os.system("python .\innosoft_api\manage.py makemigrations participacion")
os.system("python .\innosoft_api\manage.py migrate participacion")
os.system("python .\innosoft_api\manage.py createAdmin")
os.system("python .\innosoft_api\manage.py runserver")
        