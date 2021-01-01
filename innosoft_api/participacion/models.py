from django.db import models
from programa.models import Ponencia
#Descomentar cuando este importado el custom user
#from registro.models import User

#Eliminar cuando este importado el custom user
from django.contrib.auth.models import User
from .qr_base64 import qr_in_base64

class Asistencia(models.Model):
    asiste = models.BooleanField(default=False, null=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    ponencia = models.ForeignKey(Ponencia, on_delete=models.CASCADE)
    #qr = models.ImageField(blank=True, upload_to="qr_codes")
    qr_b64 = models.TextField(blank=True, unique=True)

    class Meta:
        """docstring"""
        unique_together = ["ponencia", "usuario"]

    def __str__(self):
        """docstring"""
        return str(self.usuario) + toString(self.asiste) + " a " + str(self.ponencia)

    def save(self, *args, **kwargs):

        uncoded_string = "Usuario%s Ponencia%s" % (self.usuario.pk, self.ponencia.pk)

        self.qr_b64 = qr_in_base64(uncoded_string)

        #TODO
        #coded_string = encode (uncoded_string)
        #self.qr_b64 = qr_in_base64(coded_string)

        super().save(*args, **kwargs)


def toString(self):
        result = models.CharField
        if self == False:
            result = " no asiste"
        else:
            result = " asiste"
        return result