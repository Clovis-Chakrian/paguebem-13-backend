from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Devedor, Pagamento, Conta
from ..serializers import PagamentoSerializer
from django.db.models import Avg
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Avg, Count, StdDev
import datetime
from django.core.paginator import Paginator

@swagger_auto_schema(method = 'GET')
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

    def receber_pagamento(self, pagamento):
        """
        Atualiza o índice de pagamento com base em um novo pagamento recebido.
        """
        conta = pagamento.conta
        media_tempo_pagamento = conta.pagamento_set.aggregate(Avg('tempo_para_pagar'))['tempo_para_pagar__avg']
        
        indice_pagamento = self.calcular_indice_pagamento(media_tempo_pagamento)

        conta.i_pag = indice_pagamento
        conta.save()

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
            contas = Paginator(Conta.objects.all(), 10)
            print(f'Número de contas: {contas.page(1).object_list.count()}')

        total_media = 0
        total_contas = contas.page(1).object_list.count()

        print(f'\niniciou: {datetime.datetime.now()}')
        for conta in contas.page(1).object_list:
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
        print(f'\nfinalizou: {datetime.datetime.now()}')

        # Calcular média geral se houver contas
        if total_contas > 0:
            resultado['media_geral'] = total_media / total_contas
        
        resultado['total_contas'] = total_contas

        if resultado['contas']:
            return Response(resultado, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Nenhum pagamento encontrado'}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(method='GET')
class IndiceRegularidadeView(APIView):
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
        if devedor_id:
            try:
                Devedor.objects.get(devedor_id=devedor_id)
            except Devedor.DoesNotExist:
                return Response({'error': 'Devedor não encontrado'}, status=status.HTTP_404_NOT_FOUND)

            resultado = (
                Pagamento.objects.filter(conta__devedor__devedor_id=devedor_id)
                .values('conta_id')
                .annotate(
                    desvio_padrao=StdDev('tempo_para_pagar'),
                    quantidade_pagamentos=Count('conta_id')
                )
            )
        else:
            resultado = (
                Pagamento.objects.values('conta_id', 'conta__devedor__devedor_id')
                .annotate(
                    desvio_padrao=StdDev('tempo_para_pagar'),
                    quantidade_pagamentos=Count('conta_id')
                )
            )

        indices = []
        for row in resultado:
            desvio_padrao = row.get('desvio_padrao', 0) or 0  # Ajuste caso o valor não exista
            indice_regularidade = self.calcular_indice_regularidade(desvio_padrao)
            
            try:
                conta = Conta.objects.get(id=row['conta_id'])  # Certifique-se que 'conta_id' está correto
                conta.i_reg = indice_regularidade
                conta.save()
            except Conta.DoesNotExist:
                continue 

            indices.append({
                'identificador': row['conta_id'],
                'devedor_id': row.get('conta__devedor__devedor_id', devedor_id),  # Inclui devedor_id
                'desvio_padrao': desvio_padrao,
                'quantidade_pagamentos': row['quantidade_pagamentos'],
                'indice_regularidade': indice_regularidade
            })

        total_contas = len(indices)
        media_desvio_padrao = sum(item['desvio_padrao'] for item in indices) / total_contas if total_contas else 0
        media_indice_regularidade = sum(item['indice_regularidade'] for item in indices) / total_contas if total_contas else 0

        response_data = {
            'indices': indices,
            'total_contas': total_contas,
            'media_desvio_padrao': media_desvio_padrao,
            'media_indice_regularidade': media_indice_regularidade
        }

        return Response(response_data, status=status.HTTP_200_OK)

class IndiceInteracaoView(APIView):
    """
    View para calcular o índice de interação dos devedores com base na média de leads.
    """

    def calcular_indice_interacao(self, media_lead):
        """
        Calcula o índice de interação baseado na média do lead.
        Valores possíveis:
            - 0: Frio
            - 3.333: Aquecendo
            - 6.666: Quente
            - 10: Convertido
        """
        return round(media_lead * 3.333, 2)

    def calcular_media_lead_por_conta(self, conta):
        """
        Calcula a média de lead para uma conta específica.
        """
        media_lead = conta.pagamento_set.aggregate(Avg('lead'))['lead__avg']
        return media_lead

    @swagger_auto_schema(operation_description="Atualizar índice de interação ao receber um novo lead.")
    def receber_lead(self, pagamento):
        """
        Atualiza o índice de interação com base em um novo lead recebido.
        """
        conta = pagamento.conta
        media_lead = self.calcular_media_lead_por_conta(conta)
        indice_interacao = self.calcular_indice_interacao(media_lead)

        conta.i_reg = indice_interacao
        conta.save()
             

        print(f"Índice de interação atualizado para conta {conta.conta_id}: {indice_interacao}")
        return indice_interacao

    def get(self, request, devedor_id=None):
        """
        Método GET para obter o índice de interação.
        Se `devedor_id` for fornecido, retorna apenas o índice das contas desse devedor.
        Caso contrário, retorna o índice para todos os devedores.
        """
        resultado = {
            'contas': [],
            'total_contas': 0,
            'media_geral': 0
        }

        if devedor_id:
            try:
                devedor = Devedor.objects.get(devedor_id=devedor_id)
                contas = Conta.objects.filter(devedor=devedor)
            except Devedor.DoesNotExist:
                return Response({'error': 'Devedor não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        else:
            contas = Conta.objects.all()

        total_interacao = 0
        total_contas = contas.count()

        for conta in contas:
            media_lead = self.calcular_media_lead_por_conta(conta)
            if media_lead is not None:
                indice_interacao = self.calcular_indice_interacao(media_lead)
                resultado['contas'].append({
                    'conta_id': conta.conta_id,
                    'devedor_id': conta.devedor.devedor_id,
                    'media_lead': media_lead,
                    'indice_interacao': indice_interacao
                })
                total_interacao += indice_interacao

        if total_contas > 0:
            resultado['media_geral'] = total_interacao / total_contas

        resultado['total_contas'] = total_contas

        if resultado['contas']:
            return Response(resultado, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Nenhum dado de interação encontrado'}, status=status.HTTP_404_NOT_FOUND)
        

class IndiceReputacaoView(APIView):
    """
    View para calcular o índice de reputação dos devedores com base nos índices de pagamento, regularidade e interação.
    """

    def calcular_indice_reputacao(self, i_pag, i_reg, i_int):
        """
        Calcula o índice de reputação (I.Rep) com base nos índices:
        - I_Pag: Índice de pagamento
        - I_Reg: Índice de regularidade
        - I_Int: Índice de interação
        """
        return ((i_pag * 5) + (i_reg * 3) + (i_int * 2)) / 10

    def get_indices_por_conta(self, conta):
        """
        Obtém os índices de pagamento, regularidade e interação para uma conta específica.
        """
        i_pag = conta.i_pag
        i_reg = conta.i_reg
        i_int = conta.i_int
        return i_pag, i_reg, i_int

    def calcular_indice_reputacao_para_contas(self, contas):
        """
        Calcula o índice de reputação para uma lista de contas.
        """
        resultado = []
        total_reputacao = 0

        for conta in contas:
            i_pag, i_reg, i_int = self.get_indices_por_conta(conta)

            if None not in (i_pag, i_reg, i_int):
                i_rep = self.calcular_indice_reputacao(i_pag, i_reg, i_int)
                devedor = conta.devedor
                devedor.i_reg = i_reg

                resultado.append({
                    'conta_id': conta.conta_id,
                    'devedor_id': conta.devedor.devedor_id,
                    'i_pag': i_pag,
                    'i_reg': i_reg,
                    'i_int': i_int,
                    'i_rep': i_rep
                })
                total_reputacao += i_rep

        return resultado, total_reputacao

    def get(self, request, devedor_id=None):
        """
        Método GET para obter o índice de reputação.
        Se `devedor_id` for fornecido, retorna o índice de reputação apenas das contas desse devedor.
        Caso contrário, retorna o índice para todas as contas.
        """
        resultado = {
            'contas': [],
            'total_contas': 0,
            'media_geral_reputacao': 0
        }

        if devedor_id:
            try:
                devedor = Devedor.objects.get(devedor_id=devedor_id)
                contas = Conta.objects.filter(devedor=devedor)
            except Devedor.DoesNotExist:
                return Response({'error': 'Devedor não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        else:
            contas = Conta.objects.all()

        total_contas = contas.count()
        contas_reputacao, total_reputacao = self.calcular_indice_reputacao_para_contas(contas)

        if total_contas > 0:
            resultado['media_geral_reputacao'] = total_reputacao / total_contas

        resultado['contas'] = contas_reputacao
        resultado['total_contas'] = total_contas

        if resultado['contas']:
            return Response(resultado, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Nenhum índice de reputação encontrado'}, status=status.HTTP_404_NOT_FOUND)