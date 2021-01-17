from rest_framework import serializers
from .models import Asistencia

class AsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        """
        meta for asistencia serializer
        """
        model = Asistencia
        fields = ['asiste', 'usuario', 'ponencia', 'id']

class AsistenciaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asistencia
        fields = ['ponencia', 'id']

class CodeSerializer (serializers.Serializer):
    code = serializers.CharField(max_length=200)
    ponenciaId = serializers.IntegerField()

class QRSerializer (serializers.Serializer):
    qr = serializers.CharField(max_length=200)

