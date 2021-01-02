from django.db import models
from django.conf import settings
from programa.models import Ponencia
#Descomentar cuando este importado el custom user
#from registro.models import User

#Eliminar cuando este importado el custom user
from registro.models import User

class Asistencia(models.Model):
    asiste = models.BooleanField(default=False, null=False)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ponencia = models.ForeignKey(Ponencia, on_delete=models.CASCADE)

    class Meta:
        """docstring"""
        unique_together = ["ponencia", "usuario"]

    def __str__(self):
        """docstring"""
        return str(self.usuario) + toString(self.asiste) + " a " + str(self.ponencia)


def toString(self):
        result = models.CharField
        if self == False:
            result = " no asiste"
        else:
            result = " asiste"
        return result