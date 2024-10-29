from rest_framework import generics
from .serializers import *
from .models import *


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
