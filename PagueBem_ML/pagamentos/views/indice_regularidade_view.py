from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg, Count, StdDev
from ..models import Pagamento, Devedor

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

        return Response(indices, status=status.HTTP_200_OK)
