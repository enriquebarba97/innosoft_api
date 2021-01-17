from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

GROUPS = ['administrador','moderador','staff','participante']
class Command(BaseCommand):
    help = 'Creates groups for system'
    def handle(self, *args, **options):
        for group in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group)