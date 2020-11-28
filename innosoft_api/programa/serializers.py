from rest_framework import serializers

from .models import *

class PonenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ponente
        fields = ['id', 'name', 'surname', 'phone', 'email']

class PonenciaSerializer(serializers.ModelSerializer):
#    datos_ponentes = PonenteSerializer(many=True)
    class Meta:
        model = Ponencia
        fields =['id', 'name', 'ponentes', 'description', 'time', 'place']
        # extra_kwargs = {
        #     'ponente': {'lookup_field': 'id'}
        # }
    def to_representation(self, instance):
        self.fields['ponentes'] =  PonenteSerializer(many=True)
        return super(PonenciaSerializer, self).to_representation(instance)