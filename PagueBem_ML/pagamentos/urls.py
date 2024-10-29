from django.urls import path
from .views import *

urlpatterns = [
    path('devedores/', DevedorList.as_view(), name='devedor-list'),
    path('devedores/<int:pk>/', DevedorDetail.as_view(), name='devedor-detail'),

    path('credores/', CredorList.as_view(), name='credor-list'),
    path('credores/<int:pk>/', CredorDetail.as_view(), name='credor-detail'),

    path('contas/', ContaList.as_view(), name='conta-list'),
    path('contas/<int:pk>/', ContaDetail.as_view(), name='conta-detail'),

    path('pagamentos/', PagamentoList.as_view(), name='pagamento-list'),
    path('pagamentos/<int:pk>/', PagamentoDetail.as_view(), name='pagamento-detail'),
]
