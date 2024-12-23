from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Devedor, Pagamento, Conta
from django.db.models import Avg
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Avg, Count, StdDev
import datetime

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

        if media_tempo_pagamento is not None:
            indice_pagamento = self.calcular_indice_pagamento(media_tempo_pagamento)
            conta.i_pag = indice_pagamento
            conta.save()
            print(f"Índice de pagamento atualizado para conta {conta.conta_id}: {indice_pagamento}")
        return conta.i_pag

    def get(self, request, devedor_id=None, conta_id=None):
        """
        Método GET para obter o índice de pagamento.
        Se `devedor_id` for fornecido, retorna apenas o índice das contas desse devedor.
        Se `conta_id` for fornecido, retorna o índice para a conta específica.
        Caso contrário, retorna o índice para todos os devedores.
        """
        resultado = {
            'contas': [],
            'total_contas': 0,
            'media_geral': 0
        }

        if conta_id:
            # Busca o índice para uma conta específica
            try:
                conta = Conta.objects.get(conta_id=conta_id)
                media_tempo_pagamento = conta.pagamento_set.aggregate(Avg('tempo_para_pagar'))['tempo_para_pagar__avg']

                #criar lógica de pegar o índice no banco

                if media_tempo_pagamento is not None:
                    indice_pagamento = self.calcular_indice_pagamento(media_tempo_pagamento)
                    resultado['contas'].append({
                        'conta_id': conta.conta_id,
                        'devedor_id': conta.devedor.devedor_id,
                        'media_tempo_pagamento': media_tempo_pagamento,
                        'indice_pagamento': indice_pagamento
                    })
                    resultado['total_contas'] = 1
                    resultado['media_geral'] = indice_pagamento
                else:
                    return Response({'error': 'Nenhum pagamento encontrado para a conta especificada'}, status=status.HTTP_404_NOT_FOUND)

            except Conta.DoesNotExist:
                return Response({'error': 'Conta não encontrada'}, status=status.HTTP_404_NOT_FOUND)

        else:
            # Busca contas do devedor, se fornecido
            if devedor_id:
                try:
                    devedor = Devedor.objects.get(devedor_id=devedor_id)
                    contas = Conta.objects.filter(devedor=devedor).annotate(media_tempo_pagamento=Avg('pagamento__tempo_para_pagar'))
                except Devedor.DoesNotExist:
                    return Response({'error': 'Devedor não encontrado'}, status=status.HTTP_404_NOT_FOUND)
            else:
                # Busca todas as contas e calcula a média de tempo de pagamento
                contas = Conta.objects.all().annotate(media_tempo_pagamento=Avg('pagamento__tempo_para_pagar'))

            total_media = 0
            total_contas = contas.count()

            print(f'\niniciou: {datetime.datetime.now()}')

            for conta in contas:
                media_tempo_pagamento = conta.media_tempo_pagamento
                if media_tempo_pagamento is not None:
                    if conta.i_pag is None:  # Verifica se o índice já foi calculado
                        indice_pagamento = self.calcular_indice_pagamento(media_tempo_pagamento)
                        conta.i_pag = indice_pagamento
                        conta.save()
                        print('Índice de pagamento calculado e salvo.')
                    else:
                        print('Índice de pagamento já existente, não será recalculado.')

                    resultado['contas'].append({
                        'conta_id': conta.conta_id,
                        'devedor_id': conta.devedor.devedor_id,
                        'media_tempo_pagamento': media_tempo_pagamento,
                        'indice_pagamento': conta.i_pag  # Retorna o índice atual (calculado ou já existente)
                    })
                    total_media += conta.i_pag


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

        print(f'\niniciou: {datetime.datetime.now()}')
        for row in resultado:
            desvio_padrao = row.get('desvio_padrao', 0) or 0
            indice_regularidade = self.calcular_indice_regularidade(desvio_padrao)
            
            try:
                conta = Conta.objects.get(conta_id=row['conta_id']) 
                 # Certifique-se que 'conta_id' está correto
                if conta.i_reg is None:  # Verifica se o índice de regularidade já foi calculado
                    indice_regularidade = self.calcular_indice_regularidade(desvio_padrao)
                    conta.i_reg = indice_regularidade
                    conta.save()
                    print('Índice de regularidade calculado e salvo.')
                else:
                    print('Índice de regularidade já existente, não será recalculado.')

            except Conta.DoesNotExist:
                continue 

            indices.append({
                'identificador': conta.conta_id,
                'devedor_id': row.get('conta__devedor__devedor_id', devedor_id),
                'desvio_padrao': desvio_padrao,
                'quantidade_pagamentos': row['quantidade_pagamentos'],
                'indice_regularidade': conta.i_reg  # Retorna o índice atual
            })
        print(f'\nfinalizou: {datetime.datetime.now()}')

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
        """
        return round(media_lead * 3.333, 2)

    def calcular_media_lead_por_conta(self, conta):
        """
        Calcula a média de lead para uma conta específica.
        """
        if conta.media_lead is not None:
            return conta.media_lead

        # Calcula a média de leads
        media_lead = conta.pagamento_set.aggregate(Avg('lead'))['lead__avg']
        if media_lead is not None:
            conta.media_lead = media_lead
            conta.save(update_fields=['media_lead'])  # Salva apenas a média
        return media_lead

    def calcular_media_lead_devedor(self, devedor):
        """
        Calcula a média das médias de lead das contas de um devedor.
        """
        contas = Conta.objects.filter(devedor=devedor)
        total_media_lead = 0
        total_contas = contas.count()

        for conta in contas:
            media_lead = self.calcular_media_lead_por_conta(conta)  # Certifique-se de que a média de lead da conta é calculada
            if media_lead is not None:
                total_media_lead += media_lead

        if total_contas > 0:
            media_lead_devedor = total_media_lead / total_contas
            devedor.lead = media_lead_devedor  # Atualiza o campo 'lead' do devedor
            devedor.save(update_fields=['lead'])  # Salva o valor calculado no campo 'lead'
            print(f"Média de leads do devedor {devedor.devedor_id} calculada e salva: {media_lead_devedor}")
            return media_lead_devedor
        else:
            print(f"Devedor {devedor.devedor_id} não possui contas associadas")
            return None

    def receber_lead(self, pagamento):
        """
        Atualiza o índice de interação com base em um novo lead recebido.
        """
        conta = pagamento.conta
        media_lead = self.calcular_media_lead_por_conta(conta)
        indice_interacao = self.calcular_indice_interacao(media_lead)

        conta.i_int = indice_interacao
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

        print(f'\niniciou: {datetime.datetime.now()}')

        for conta in contas:
            # Verifica se o índice de interação já está calculado
            devedor = conta.devedor
            if conta.i_int is None:  # Verifica se o campo está nulo no banco
                media_lead = self.calcular_media_lead_por_conta(conta)
                devedor.lead = self.calcular_media_lead_devedor(devedor)
                if media_lead is not None:  # Apenas calcula se a média de leads está disponível
                    indice_interacao = self.calcular_indice_interacao(media_lead)
                    conta.i_int = indice_interacao
                    conta.save()
                    print('Mais um índice salvo')
                    resultado['contas'].append({
                        'conta_id': conta.conta_id,
                        'devedor_id': conta.devedor.devedor_id,
                        'media_lead': media_lead,
                        'indice_interacao': indice_interacao
                    })
                    total_interacao += indice_interacao
            else:
                # Índice já está calculado, apenas retorna o valor existente
                print(f"Índice de interação já calculado para a conta {conta.conta_id}")
                resultado['contas'].append({
                    'conta_id': conta.conta_id,
                    'devedor_id': conta.devedor.devedor_id,
                    'media_lead': conta.media_lead,  # Usa o valor existente no banco
                    'indice_interacao': conta.i_int  # Retorna o valor do banco
                })

        # Após calcular e salvar a média de lead do devedor
        if devedor_id:
            resultado['media_lead_devedor'] = devedor.lead

        print(f'\nfinalizou: {datetime.datetime.now()}')

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

    def get(self, request, devedor_id=None):
        """
        Método GET para obter o índice de reputação.
        Se `devedor_id` for fornecido, retorna o índice de reputação apenas das contas desse devedor
        e salva a média como o índice de reputação do devedor.
        Caso contrário, retorna o índice para todas as contas.
        """
        resultado = {
            'indices': [],
            'total_contas': 0,
            'media_reputacao': 0
        }

        # Filtra contas por devedor ou todas
        if devedor_id:
            try:
                devedor = Devedor.objects.get(devedor_id=devedor_id)
                contas = Conta.objects.filter(devedor=devedor)
            except Devedor.DoesNotExist:
                return Response({'error': 'Devedor não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        else:
            contas = Conta.objects.all()

        total_contas = contas.count()
        indices_reputacao = []
        total_reputacao = 0

        print(f'\nInício do processamento: {datetime.datetime.now()}')

        for conta in contas:
    # Verifica se o índice de reputação já está calculado
            if conta.i_rep is None:  # Apenas calcula se o índice de reputação está nulo
                i_pag = conta.i_pag
                i_reg = conta.i_reg
                i_int = conta.i_int

                if None not in (i_pag, i_reg, i_int):  # Certifica que todos os índices necessários estão presentes
                    i_rep = self.calcular_indice_reputacao(i_pag, i_reg, i_int)
                    conta.i_rep = i_rep  # Atualiza o índice de reputação
                    conta.save()  # Salva a conta com o novo índice de reputação
                    indices_reputacao.append({
                        'conta_id': conta.conta_id,
                        'devedor_id': conta.devedor.devedor_id,
                        'i_pag': i_pag,
                        'i_reg': i_reg,
                        'i_int': i_int,
                        'i_rep': i_rep
                    })
                    total_reputacao += i_rep
            else:
                # Índice de reputação já calculado, apenas retorna o valor existente
                print(f"Índice de reputação já calculado para a conta {conta.conta_id}")
                indices_reputacao.append({
                    'conta_id': conta.conta_id,
                    'devedor_id': conta.devedor.devedor_id,
                    'i_pag': conta.i_pag,
                    'i_reg': conta.i_reg,
                    'i_int': conta.i_int,
                    'i_rep': conta.i_rep  # Retorna o valor do banco
                })
                total_reputacao += conta.i_rep  # Adiciona o índice existente ao total


        print(f'\nFim do processamento: {datetime.datetime.now()}')

        # Cálculo e atualização do índice de reputação do devedor, se aplicável
        if devedor_id and total_contas > 0:
            media_reputacao = total_reputacao / total_contas
            devedor.indice_reputacao = media_reputacao
            devedor.save()  # Salva o índice de reputação do devedor
            resultado['media_reputacao'] = media_reputacao
        
        if  total_contas > 0:
            media_reputacao = total_reputacao / total_contas
            resultado['media_reputacao'] = media_reputacao

        # Atualização para a resposta final
        resultado['indices'] = indices_reputacao
        resultado['total_contas'] = total_contas

        if resultado['indices']:
            return Response(resultado, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Nenhum índice de reputação encontrado'}, status=status.HTTP_404_NOT_FOUND)
