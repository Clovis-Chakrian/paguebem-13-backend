from django.urls import path
from .views.views import *
from .views.indices_view import *
from .views.views import PagamentoList, PagamentoDetail


urlpatterns = [
    path('exemplo/', ExampleList.as_view(), name='exemplo-list'),
    path('exemplo/<int:devedor_id>/', ExampleDetail.as_view(), name='exemplo-detail'),

    path('devedores/', DevedorList.as_view(), name='devedor-list'),
    path('devedores/<int:pk>/', DevedorDetail.as_view(), name='devedor-detail'),

    path('credores/', CredorList.as_view(), name='credor-list'),
    path('credores/<int:pk>/', CredorDetail.as_view(), name='credor-detail'),

    path('contas/', ContaList.as_view(), name='conta-list'),
    path('contas/<int:pk>/', ContaDetail.as_view(), name='conta-detail'),

    path('pagamentos/', PagamentoList.as_view(), name='pagamento-list'),
    path('pagamentos/<int:pk>/', PagamentoDetail.as_view(), name='pagamento-detail'),

     # Endpoint para obter o índice de todos os devedores (GET)
    path('indice-pagamento/', IndicePagamentoView.as_view(), name='indice_pagamento_todos'),
    
    # Endpoint para registrar um novo pagamento (POST) e obter o índice de um devedor específico (GET)
    path('indice-pagamento/<int:devedor_id>/', IndicePagamentoView.as_view(), name='indice_pagamento_devedor'),
]
