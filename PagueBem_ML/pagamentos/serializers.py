from rest_framework import serializers
from .models import *

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
        


class ContaSerializer(serializers.ModelSerializer):
    i_pag = serializers.DecimalField(max_digits=4, decimal_places=2, read_only=True)

    class Meta:
        model = Conta
        fields = ['conta_id', 'devedor', 'credor', 'valor_total', 'numero_parcelas', 'i_pag', 'i_reg', 'i_int', 'i_rep']
        read_only_fields = ['conta_id', 'i_pag', 'i_reg', 'i_int', 'i_rep']

class ContaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conta
        fields = ['conta_id', 'devedor', 'credor', 'valor_total', 'numero_parcelas']
        read_only_fields = ['conta_id']

class DevedorPFSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devedor
        fields = ['devedor_id', 'tipo', 'cpf', 'nome', 'email', 'celular', 'telefone', 'indice_reputacao', 'lead']
        read_only_fields = ['devedor_id', 'indice_reputacao', 'lead']

    def create(self, validated_data):
        validated_data['tipo'] = 'PF'  # Define o tipo como Pessoa Física
        return super().create(validated_data)

class DevedorPJSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devedor
        fields = ['devedor_id', 'tipo', 'cnpj', 'razao_social', 'nome_fantasia', 'email', 'celular', 'telefone', 'indice_reputacao', 'lead']
        read_only_fields = ['devedor_id', 'indice_reputacao', 'lead']
    
    def create(self, validated_data):
        validated_data['tipo'] = 'PJ'  # Define o tipo como Pessoa Jurídica
        return super().create(validated_data)


# Serializers para Credor
class CredorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credor
        fields = ['id', 'nome', 'email', 'tipo', 'cpf', 'cnpj']  # Inclua campos genéricos


class CredorPFSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credor
        fields = ['id', 'tipo', 'cpf', 'nome', 'email', 'celular', 'telefone', 'password', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True},
        }
        read_only_fields = ['id']

    def create(self, validated_data):
        credor = Credor.objects.create_user(**validated_data)
        return credor

class CredorPJSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credor
        fields = ['id', 'tipo', 'cnpj', 'razao_social', 'nome_fantasia', 'email', 'celular', 'telefone', 'password', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True},
        }
        read_only_fields = ['id']

    def create(self, validated_data):
        credor = Credor.objects.create_user(**validated_data)
        return credor
    
class PagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pagamento
        fields = [
            'pagamento_id', 
            'conta',
            'devedor',
            'credor',
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
