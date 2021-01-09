from django.core.management.base import BaseCommand
from registro.models import User
from django.contrib.auth.models import Group
from django.db import IntegrityError


class Command(BaseCommand):
    help = 'Creates admin user'

    #uvus: admin  pass: admin

    def handle(self, *args, **kwargs):

        if (not User.objects.filter(uvus="admin").exists()):
            user= User.objects.create(uvus="admin",email="", first_name="admin",last_name="admin")
            user.set_password("admin")
            user.is_staff = True
            user.is_superuser = True
            user.save()
            group = Group.objects.get(id=1)
            user.groups.add(group)

        

            