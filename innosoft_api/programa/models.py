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
    name = models.CharField(max_length=80)
    ponentes = models.ManyToManyField(Ponente, related_name='datos_ponentes')
    description = models.CharField(max_length=2000)
    time = models.DateTimeField()
    place = models.CharField(max_length=20)

    def __str__(self):
        return self.name