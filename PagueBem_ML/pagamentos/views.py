from rest_framework import generics
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status


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

class PagamentoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer

##Métodos de exemplo usando as conveções
# Classe para listar e criar novos devedores
class ExampleList(generics.ListCreateAPIView):
    queryset = Devedor.objects.all()
    serializer_class = DevedorCadastroSerialzer

# Classe para obter, atualizar e deletar um devedor específico
class ExampleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Devedor.objects.all()
    serializer_class = DevedorCadastroSerialzer
    lookup_field = 'devedor_id'  # Especifica o campo 'devedor_id' para busca

# @csrf_exempt  # Para desativar a proteção CSRF (não recomendado em produção)
# @swagger_auto_schema(method='POST', request_body=DevedorCadastroSerialzer) #para sinalizar para o swagger que função mapeia métodos post e qual parametro o body precisa para criação
# @api_view(['GET', 'POST'])
# def devedor_list_2(request):
#     if request.method == 'GET':
#         devedores = Devedor.objects.all()
#         serializer = DevedorCadastroSerialzer(devedores, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = DevedorCadastroSerialzer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @csrf_exempt
# @swagger_auto_schema(method='put', request_body=DevedorCadastroSerialzer)
# @api_view(['GET', 'PUT', 'DELETE'])
# def devedor_detail_2(request, id):
#     try:
#         devedor = Devedor.objects.get(devedor_id=id)
#     except Devedor.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == 'GET':
#         serializer = DevedorCadastroSerialzer(devedor)
#         return  Response(serializer.data, status=status.HTTP_200_OK)

#     elif request.method == 'PUT':
#         serializer = DevedorCadastroSerialzer(devedor, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         devedor.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
