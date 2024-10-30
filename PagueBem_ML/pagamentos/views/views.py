from rest_framework import generics
from ..serializers import *
from ..models import *

from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

class DevedorList(generics.ListCreateAPIView):
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
    serializer_class = DevedorSerializer

# Classe para obter, atualizar e deletar um devedor específico
class ExampleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Devedor.objects.all()
    serializer_class = DevedorSerializer
    lookup_field = 'devedor_id'  # Especifica o campo 'devedor_id' para busca


@swagger_auto_schema(method='POST', request_body=DevedorCadastroSerialzer) #para sinalizar para o swagger que função mapeia métodos post e qual parametro o body precisa para criação
@api_view(['GET', 'POST'])
def devedor_list_2(request):
    if request.method == 'GET':
        devedores = Devedor.objects.all()
        serializer = DevedorCadastroSerialzer(devedores, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DevedorCadastroSerialzer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





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
