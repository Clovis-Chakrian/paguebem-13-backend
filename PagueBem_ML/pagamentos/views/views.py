from rest_framework import generics
from ..serializers import *
from ..models import *
from .indices_view import IndicePagamentoView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


class LoginView(APIView):
    # permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        # Autentica o usuário usando o email e a senha
        user = authenticate(email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": "Credenciais inválidas."},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class ContaList(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]  # Exemplo de autenticação

    queryset = Conta.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":  # Usar serializer de criação para POST
            return ContaCreateSerializer
        return ContaSerializer


class ContaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Conta.objects.all()
    serializer_class = ContaSerializer


# View para listar todos os devedores com base no tipo
class DevedorListView(APIView):
    """
    View para listar todos os devedores utilizando serializers específicos com base no tipo.
    """

    def get(self, request, *args, **kwargs):
        # Recupera todos os devedores
        devedores = Devedor.objects.all()
        serialized_data = []

        # Processa cada devedor individualmente
        for devedor in devedores:
            if devedor.tipo == "PF":
                serializer = DevedorPFSerializer(devedor)
            elif devedor.tipo == "PJ":
                serializer = DevedorPJSerializer(devedor)
            else:
                continue  # Ignora tipos desconhecidos
            serialized_data.append(serializer.data)

        # Retorna os dados serializados
        return Response(serialized_data)


# View para detalhar um devedor com base no tipo
class DevedorDetailView(generics.RetrieveAPIView):
    """
    View para buscar detalhes de um devedor específico pelo ID.
    """

    queryset = Devedor.objects.all()

    def get_serializer_class(self):
        """
        Seleciona o serializer com base no tipo do devedor.
        """
        devedor = self.get_object()
        if devedor.tipo == "PF":
            return DevedorPFSerializer
        return DevedorPJSerializer


# View para listar e criar devedores do tipo Pessoa Física (PF)
class DevedorPFListCreateView(generics.ListCreateAPIView):
    """
    View para listar e criar devedores do tipo Pessoa Física.
    """

    queryset = Devedor.objects.filter(tipo="PF")
    serializer_class = DevedorPFSerializer


# View para detalhar, atualizar ou deletar um devedor Pessoa Física (PF)
class DevedorPFDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View para obter, atualizar ou deletar um devedor Pessoa Física.
    """

    queryset = Devedor.objects.filter(tipo="PF")
    serializer_class = DevedorPFSerializer


# View para listar e criar devedores do tipo Pessoa Jurídica (PJ)
class DevedorPJListCreateView(generics.ListCreateAPIView):
    """
    View para listar e criar devedores do tipo Pessoa Jurídica.
    """

    queryset = Devedor.objects.filter(tipo="PJ")
    serializer_class = DevedorPJSerializer


# View para detalhar, atualizar ou deletar um devedor Pessoa Jurídica (PJ)
class DevedorPJDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View para obter, atualizar ou deletar um devedor Pessoa Jurídica.
    """

    queryset = Devedor.objects.filter(tipo="PJ")
    serializer_class = DevedorPJSerializer


# View para listar todos os devedores, diferenciando pelo tipo
class DevedorListView(APIView):
    """
    View para listar todos os devedores, utilizando serializers específicos com base no tipo.
    """

    def get(self, request, *args, **kwargs):
        # Recupera todos os devedores
        devedores = Devedor.objects.all()
        serialized_data = []

        # Processa cada devedor individualmente
        for devedor in devedores:
            if devedor.tipo == "PF":
                serializer = DevedorPFSerializer(devedor)
            elif devedor.tipo == "PJ":
                serializer = DevedorPJSerializer(devedor)
            else:
                continue  # Ignora tipos desconhecidos
            serialized_data.append(serializer.data)

        # Retorna os dados serializados
        return Response(serialized_data)

# Views para Credor


class CredorListView(APIView):
    """
    View para listar todos os credores utilizando serializers específicos com base no tipo.
    """

    def get(self, request, *args, **kwargs):
        # Recupera todos os credores
        credores = Credor.objects.all()
        serialized_data = []

        # Processa cada credor individualmente
        for credor in credores:
            if credor.tipo == "PF":
                serializer = CredorPFSerializer(credor)
            elif credor.tipo == "PJ":
                serializer = CredorPJSerializer(credor)
            else:
                continue  # Ignora tipos desconhecidos
            serialized_data.append(serializer.data)

        # Retorna os dados serializados
        return Response(serialized_data)


class CredorDetailView(generics.RetrieveAPIView):
    """
    View para buscar detalhes de um credor específico pelo ID.
    """

    queryset = Credor.objects.all()

    def get_serializer_class(self):
        """
        Seleciona o serializer com base no tipo do credor.
        """
        credor = self.get_object()
        if credor.tipo == "PESSOA_FISICA":
            return CredorPFSerializer
        return CredorPJSerializer


class CredorPFListCreateView(generics.ListCreateAPIView):
    queryset = Credor.objects.filter(tipo="PESSOA_FISICA")
    serializer_class = CredorPFSerializer


class CredorPFDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Credor.objects.filter(tipo="PESSOA_FISICA")
    serializer_class = CredorPFSerializer


class CredorPJListCreateView(generics.ListCreateAPIView):
    queryset = Credor.objects.filter(tipo="PESSOA_JURIDICA")
    serializer_class = CredorPJSerializer


class CredorPJDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Credor.objects.filter(tipo="PESSOA_JURIDICA")
    serializer_class = CredorPJSerializer


class CredorPFListView(generics.ListAPIView):
    """
    View para listar apenas credores do tipo Pessoa Física.
    """

    serializer_class = CredorPFSerializer

    def get_queryset(self):
        return Credor.objects.filter(tipo="PF")


class CredorPJListView(generics.ListAPIView):
    """
    View para listar apenas credores do tipo Pessoa Jurídica.
    """

    serializer_class = CredorPJSerializer

    def get_queryset(self):
        return Credor.objects.filter(tipo="PJ")


class PagamentoList(generics.ListCreateAPIView):
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer

    def perform_create(self, serializer):
        # Salva o novo pagamento
        pagamento = serializer.save()

        # Chama o método que está em PagamentoDetail para realizar uma ação
        indice_pagamento = IndicePagamentoView()
        indice_pagamento.calcular_indice_pagamento(pagamento)


class PagamentoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer


class PagamentoListCredor(generics.ListAPIView):
    serializer_class = PagamentoSerializer

    def get_queryset(self):
        email_credor = self.kwargs.get("email")  # Captura o e-mail do credor da URL
        try:
            credor = Credor.objects.get(email=email_credor)
            return credor.pagamento.all()  # Retorna todos os pagamentos do credor
        except Credor.DoesNotExist:
            return (
                Pagamento.objects.none()
            )  # Retorna um queryset vazio se o credor não existir


##Métodos de exemplo usando as conveções
# Classe para listar e criar novos devedores
# class ExampleList(generics.ListCreateAPIView):
#     queryset = Devedor.objects.all()
#     serializer_class = DevedorSerializer

# # Classe para obter, atualizar e deletar um devedor específico
# class ExampleDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Devedor.objects.all()
#     serializer_class = DevedorSerializer
#     lookup_field = 'devedor_id'  # Especifica o campo 'devedor_id' para busca


# @csrf_exempt  # Para desativar a proteção CSRF (não recomendado em produção)
# @swagger_auto_schema(method='POST', request_body=DevedorCadastroSerialzer) #para sinalizar para o swagger que função mapeia métodos post e qual parametro o body precisa para criação
# @api_view(['GET', 'POST'])
