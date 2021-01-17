from django.db import models
from phone_field import PhoneField

# Create your models here.
class Ponente(models.Model):
    name = models.CharField(max_length=80)
    surname = models.CharField(max_length=80,blank=True)
    phone = PhoneField(blank=True)
    email = models.EmailField(max_length=254,blank=True)
    

    def __str__(self):
        return self.name

class Ponencia(models.Model):
    CATEGORIAS = (
        ('IA', 'Inteligencia articial'),
        ('ODOO', 'Odoo'),
        ('PRG', 'Programacion'),
        ('OTH', 'Otras'),
        )
    name = models.CharField(max_length=80)
    ponentes = models.ManyToManyField(Ponente, related_name='datos_ponentes')
    description = models.CharField(max_length=2000)
    time = models.DateTimeField()
    place = models.CharField(max_length=20)
    categoria = models.CharField(max_length=35, choices=CATEGORIAS, default='Otras')

    def __str__(self):
        return self.name