from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Devedor, Pagamento, Conta
from ..serializers import PagamentoSerializer
from django.db.models import Avg
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Avg, Count, StdDev


class IndicePagamentoView(APIView):
    """
    View para calcular o índice de pagamento por devedor, agrupado por conta.
    """

    def calcular_indice_pagamento(self, media):
        # Retorna o índice de acordo com a média
        if media < -15:
            return 0
        elif -15 <= media < -10:
            return 2.5
        elif -10 <= media < -5:
            return 5.0
        elif -5 <= media < -2:
            return 7.0
        elif -2 <= media < 0:
            return 8
        elif media >= 0:
            return 10

    @swagger_auto_schema(request_body=PagamentoSerializer)
    def receber_pagamento(self, pagamento):
        """
        Atualiza o índice de pagamento com base em um novo pagamento recebido.
        """
        conta = pagamento.conta
        media_tempo_pagamento = conta.pagamento_set.aggregate(Avg('tempo_para_pagar'))['tempo_para_pagar__avg']
        
        indice_pagamento = self.calcular_indice_pagamento(media_tempo_pagamento)

        print(f"Índice de pagamento atualizado para conta {conta.conta_id}: {indice_pagamento}")
        return indice_pagamento 

    def get(self, request, devedor_id=None):
        """
        Método GET para obter o índice de pagamento.
        Se `devedor_id` for fornecido, retorna apenas o índice das contas desse devedor.
        Caso contrário, retorna o índice para todos os devedores.
        """
        resultado = {
            'contas': [],
            'total_contas': 0,
            'media_geral': 0
        }
        
        if devedor_id:
            # Busca as contas para um devedor específico
            try:
                devedor = Devedor.objects.get(devedor_id=devedor_id)
                contas = Conta.objects.filter(devedor=devedor)
            except Devedor.DoesNotExist:
                return Response({'error': 'Devedor não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Busca todas as contas
            contas = Conta.objects.all()

        total_media = 0
        total_contas = contas.count()

        for conta in contas:
            media_tempo_pagamento = conta.pagamento_set.aggregate(Avg('tempo_para_pagar'))['tempo_para_pagar__avg']
            if media_tempo_pagamento is not None:
                indice_pagamento = self.calcular_indice_pagamento(media_tempo_pagamento)
                resultado['contas'].append({
                    'conta_id': conta.conta_id,
                    'devedor_id': conta.devedor.devedor_id,
                    'media_tempo_pagamento': media_tempo_pagamento,
                    'indice_pagamento': indice_pagamento
                })
                total_media += indice_pagamento

        # Calcular média geral se houver contas
        if total_contas > 0:
            resultado['media_geral'] = total_media / total_contas
        
        resultado['total_contas'] = total_contas

        if resultado['contas']:
            return Response(resultado, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Nenhum pagamento encontrado'}, status=status.HTTP_404_NOT_FOUND)


class IndiceRegularidadeView(APIView):
    """
    View para calcular o índice de regularidade baseado nos pagamentos das contas de um devedor específico.
    Se nenhum devedor_id for fornecido, retorna o índice para todas as contas.
    """

    def calcular_indice_regularidade(self, desvio_padrao):
        if desvio_padrao > 30:
            return 0
        elif 20 < desvio_padrao <= 30:
            return 2.5
        elif 10 < desvio_padrao <= 20:
            return 5
        elif 5 < desvio_padrao <= 10:
            return 7
        elif 3 < desvio_padrao <= 5:
            return 8
        elif 0 <= desvio_padrao <= 3:
            return 10

    def get(self, request, devedor_id=None):
        """
        Método GET para calcular e retornar os índices de regularidade.
        Se `devedor_id` for fornecido, retorna apenas os índices das contas desse devedor.
        """
        if devedor_id:
            try:
                # Verifica se o devedor existe
                Devedor.objects.get(devedor_id=devedor_id)
            except Devedor.DoesNotExist:
                return Response({'error': 'Devedor não encontrado'}, status=status.HTTP_404_NOT_FOUND)

            resultado = (
                Pagamento.objects.filter(conta__devedor__devedor_id=devedor_id)
                .values('conta__identificador')
                .annotate(
                    desvio_padrao=StdDev('tempo_para_pagar'),
                    quantidade_pagamentos=Count('id')
                )
            )
        else:
            resultado = (
                Pagamento.objects.values('conta__identificador')
                .annotate(
                    desvio_padrao=StdDev('tempo_para_pagar'),
                    quantidade_pagamentos=Count('id')
                )
            )

        indices = []
        for row in resultado:
            desvio_padrao = row['desvio_padrao'] if row['desvio_padrao'] is not None else 0
            indice_regularidade = self.calcular_indice_regularidade(desvio_padrao)
            indices.append({
                'identificador': row['conta__identificador'],
                'desvio_padrao': desvio_padrao,
                'quantidade_pagamentos': row['quantidade_pagamentos'],
                'indice_regularidade': indice_regularidade
            })

        # Cálculo dos totais e médias
        total_contas = len(indices)
        media_desvio_padrao = sum(item['desvio_padrao'] for item in indices) / total_contas if total_contas > 0 else 0
        media_indice_regularidade = sum(item['indice_regularidade'] for item in indices) / total_contas if total_contas > 0 else 0

        # Preparando a resposta
        response_data = {
            'indices': indices,
            'total_contas': total_contas,
            'media_desvio_padrao': media_desvio_padrao,
            'media_indice_regularidade': media_indice_regularidade
        }

        return Response(response_data, status=status.HTTP_200_OK)
