from rest_framework import serializers
from .models import *

class DevedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devedor
        fields = ['devedor_id', 'indice_reputacao', 'lead']
        read_only_fields = ['devedor_id'] 


class ContaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conta
        fields = ['conta_id', 'devedor', 'credor', 'valor_total', 'numero_parcelas']
        read_only_fields = ['conta_id']


class CredorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credor
        fields = ['credor_id', 'cnpj', 'razao_social', 'nome_fantasia', 'email', 'password', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True}, 
        }
        read_only_fields = ['credor_id']

    def create(self, validated_data):
        # Cria o credor usando o manager
        credor = Credor.objects.create_user(**validated_data)
        return credor
    
class PagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pagamento
        fields = [
            'pagamento_id', 
            'conta', 
            'numero_parcela', 
            'numero_documento', 
            'vencimento', 
            'data_pagamento', 
            'tempo_para_pagar', 
            'valor_pagamento', 
            'valor_pago', 
            'diferenca_valores', 
            'lead'
        ]
        read_only_fields = ['pagamento_id']
