from rest_framework import serializers
from .models import Asistencia
from django.core.exceptions import ObjectDoesNotExist
import traceback
from django.http.response import Http404

class AsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        """docstring"""
        model = Asistencia
        fields = ['asiste', 'usuario', 'ponencia', 'id']

class AsistenciaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asistencia
        fields = ['usuario', 'ponencia', 'id']
