from rest_framework import serializers
from .models import Devedor

#exemplo inicial de serializer de Devedor, pra usarem de base
class DevedorCadastroSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Devedor
        fields = ["devedor_id", "indice_reputacao", "lead"]
