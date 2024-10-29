from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import *
from django.views.decorators.csrf import csrf_exempt
import json
from django.views import View
from django.contrib.auth.hashers import make_password


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

@csrf_exempt
@api_view(['GET', 'POST'])
def credor_view(request):
    if request.method == 'GET':
        users = Credor.objects.values()
        return JsonResponse(list(users), safe=False)

    elif request.method == 'POST':
        data = json.loads(request.body)

        # Validação simplificada
        if not all(key in data for key in ('cnpj', 'razao_social', 'nome_fantasia', 'email', 'password')):
            return JsonResponse({'error': 'Faltam campos obrigatórios.'}, status=400)

        try:
            # Criação do usuário
            user = Credor.objects.create(
                cnpj=data['cnpj'],
                razao_social=data['razao_social'],
                nome_fantasia=data['nome_fantasia'],
                email=data['email'],
                password=make_password(data['password'])  # Criptografar a senha
            )
            user_data = {
                'credor_id': user.credor_id,
            }
            return JsonResponse(user_data, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
