from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Devedor, Pagamento  # ajustado para utilizar Devedor e Pagamento
from ..serializers import PagamentoSerializer  # ajustado para utilizar DevedorSerializer
from django.db.models import Avg
from drf_yasg.utils import swagger_auto_schema

class IndicePagamentoView(APIView):
    """
    View para calcular o índice de pagamento por devedor.
    """
    
    def calcular_indice_pagamento(self, media):
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

    def tabela_indice_pagamento(self):
        # Calcula a média de tempo de pagamento por devedor a partir do banco de dados
        devedores = Devedor.objects.all()
        resultado = []
        
        for devedor in devedores:
            media_tempo_pagamento = devedor.pagamentos.aggregate(Avg('tempo_para_pagar'))['tempo_para_pagar__avg']
            if media_tempo_pagamento is not None:
                indice_pagamento = self.calcular_indice_pagamento(media_tempo_pagamento)
                resultado.append({
                    'identificador': devedor.id,
                    'media_tempo_pagamento': media_tempo_pagamento,
                    'indice_pagamento': indice_pagamento
                })

        return resultado

    @swagger_auto_schema(request_body=PagamentoSerializer)
    def post(self, request, devedor_id):
        try:
            devedor = Devedor.objects.get(id=devedor_id)
        except Devedor.DoesNotExist:
            return Response({'error': 'Devedor não encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PagamentoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        tempo_para_pagar = serializer.validated_data['tempo_para_pagar']
        pagamento = Pagamento(devedor=devedor, tempo_para_pagar=tempo_para_pagar)
        pagamento.save()

        media_tempo_pagamento = devedor.pagamentos.aggregate(Avg('tempo_para_pagar'))['tempo_para_pagar__avg']
        indice_pagamento = self.calcular_indice_pagamento(media_tempo_pagamento)

        return Response({
            'identificador': devedor.id,
            'media_tempo_pagamento': media_tempo_pagamento,
            'indice_pagamento': indice_pagamento
        }, status=status.HTTP_200_OK)

    def get(self, request, devedor_id=None):
        """
        Método GET para obter o índice de pagamento por devedor.
        Se `devedor_id` for fornecido, retorna apenas o índice desse devedor.
        """
        if devedor_id:
            try:
                devedor = Devedor.objects.get(id=devedor_id)
            except Devedor.DoesNotExist:
                return Response({'error': 'Devedor não encontrado'}, status=status.HTTP_404_NOT_FOUND)

            media_tempo_pagamento = devedor.pagamentos.aggregate(Avg('tempo_para_pagar'))['tempo_para_pagar__avg']
            if media_tempo_pagamento is not None:
                return Response({
                    'identificador': devedor.id,
                    'media_tempo_pagamento': media_tempo_pagamento,
                    'indice_pagamento': self.calcular_indice_pagamento(media_tempo_pagamento)
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Nenhum pagamento encontrado para este devedor'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Calcula o índice para todos os devedores
            resultado = self.tabela_indice_pagamento()
            return Response(resultado, status=status.HTTP_200_OK)
