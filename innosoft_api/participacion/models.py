from django.db import models
from django.conf import settings
from programa.models import Ponencia
from .cryptography import encrypt
import random


class Asistencia(models.Model):
    asiste = models.BooleanField(default=False, null=False)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ponencia = models.ForeignKey(Ponencia, on_delete=models.CASCADE)
    code = models.TextField(blank=True, unique=True)

    class Meta:
        unique_together = ["ponencia", "usuario"]
        ordering = ['id']

    def __str__(self):
        """
        Return string of asistencia
        """
        return str(self.usuario) + toString(self.asiste) + " a " + str(self.ponencia)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        uncoded_string = "Usuario%s Ponencia%s Random%d" % (self.usuario.pk, self.ponencia.pk, random.randint(1,999))

        password = str(self.usuario.id) + "" + str(self.ponencia.id)

        coded_bytes = encrypt (uncoded_string, password)

        self.code = coded_bytes

        super().save(force_insert, force_update, using, update_fields)


def toString(self):
        result = models.CharField
        if self == False:
            result = " no asiste"
        else:
            result = " asiste"
        return result