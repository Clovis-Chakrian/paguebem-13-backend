from rest_framework import generics
from ..serializers import *
from ..models import *
from .indices_view import IndicePagamentoView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.views import APIView

from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        
        # Autentica o usuário usando o email e a senha
        user = authenticate(email=email, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Credenciais inválidas."}, status=status.HTTP_401_UNAUTHORIZED)


class DevedorList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated] #Exemplo de autenticação
    queryset = Devedor.objects.all()
    serializer_class = DevedorSerializer

class DevedorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Devedor.objects.all()
    serializer_class = DevedorSerializer

class ContaList(generics.ListCreateAPIView):
    queryset = Conta.objects.all()
    serializer_class = ContaSerializer

class ContaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Conta.objects.all()
    serializer_class = ContaSerializer

class CredorList(generics.ListCreateAPIView):
    queryset = Credor.objects.all()
    serializer_class = CredorSerializer

class CredorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Credor.objects.all()
    serializer_class = CredorSerializer

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

##Métodos de exemplo usando as conveções
# Classe para listar e criar novos devedores
class ExampleList(generics.ListCreateAPIView):
    queryset = Devedor.objects.all()
    serializer_class = DevedorSerializer

# Classe para obter, atualizar e deletar um devedor específico
class ExampleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Devedor.objects.all()
    serializer_class = DevedorSerializer
    lookup_field = 'devedor_id'  # Especifica o campo 'devedor_id' para busca


# @csrf_exempt  # Para desativar a proteção CSRF (não recomendado em produção)
# @swagger_auto_schema(method='POST', request_body=DevedorCadastroSerialzer) #para sinalizar para o swagger que função mapeia métodos post e qual parametro o body precisa para criação
# @api_view(['GET', 'POST'])
