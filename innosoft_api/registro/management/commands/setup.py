from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Sets up the system'

    def handle(self, *args, **kwargs):
        call_command("makemigrations", "registro")
        call_command("migrate","registro")
        call_command("group")
        call_command("migrate")
        call_command("makemigrations", "programa")
        call_command("migrate", "programa")
        call_command("makemigrations", "participacion")
        call_command("migrate", "participacion")
        call_command("createAdmin")