from django.db import models
# Create your models here.
class Ponente(models.Model):
    name = models.CharField(max_length=80)
    age = models.IntegerField()

    def __str__(self):
        return self.name