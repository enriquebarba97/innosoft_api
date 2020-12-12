from rest_framework import serializers
from participacion.models import Asistencia
 

class AsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asistencia
        fields = ['asiste', 'usuario', 'ponencia', 'id']

class AsistenciaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asistencia
        fields = ['usuario', 'ponencia', 'id']

class AsistenciaCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asistencia
        fields = []
    def update(self, instance, validated_data):
        instance.asiste = True
        instance.save()
        return instance
