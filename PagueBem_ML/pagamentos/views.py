from django.shortcuts import render
from rest_framework import generics
from .models import Devedor
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Devedor
from django.views.decorators.csrf import csrf_exempt
import json

from .serializer import DevedorCadastroSerialzer
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

@csrf_exempt  # Para desativar a proteção CSRF (não recomendado em produção)
@api_view(['GET', 'POST'])
def devedor_list(request):
    if request.method == 'GET':
        devedores = list(Devedor.objects.values())
        return JsonResponse(devedores, safe=False)

    elif request.method == 'POST':
        data = json.loads(request.body)
        devedor = Devedor.objects.create(**data)
        return JsonResponse({'id': devedor.devedor_id}, status=201)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def devedor_detail(request, pk):
    try:
        devedor = Devedor.objects.get(devedor_id=pk)
    except Devedor.DoesNotExist:
        return JsonResponse({'error': 'Devedor não encontrado.'}, status=404)

    if request.method == 'GET':
        return JsonResponse({'id': devedor.devedor_id, 'indice_reputacao': devedor.indice_reputacao, 'lead': devedor.lead})

    elif request.method == 'PUT':
        data = json.loads(request.body)
        devedor.indice_reputacao = data.get('indice_reputacao', devedor.indice_reputacao)
        devedor.lead = data.get('lead', devedor.lead)
        devedor.save()
        return JsonResponse({'message': 'Devedor atualizado.'})

    elif request.method == 'DELETE':
        devedor.delete()
        return JsonResponse({'message': 'Devedor deletado.'})


@csrf_exempt  # Para desativar a proteção CSRF (não recomendado em produção)
@swagger_auto_schema(method='POST', request_body=DevedorCadastroSerialzer)
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
