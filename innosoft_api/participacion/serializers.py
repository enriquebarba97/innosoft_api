from rest_framework import serializers
from participacion.models import Asistencia
 

class AsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asistencia
        fields = ['asiste', 'usuario', 'ponencia']
