# paguebem-13-backend
Repositório do backend da squad 13 da PagueBem | Residência 2024.2

Passo a passo para rodar o projeto 

1. Intalar o python 3.12.1

2. Apagar a pasta .venv se existir

3. Criar um ambiente virtual localmente (“python -m venv ./env")

4. Ativar ambiente ./env/Scripts/activate” 

5. Intalar as dependências (pip install -r .\requeriments.txt)

6. Adicionar o banco postgresql no PagueBem_ML\PagueBem_ML\settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': ' ',
        'PASSWORD': ' ',
        'HOST': ' ', 
        'PORT': ' ', 
    }
}

7. Rodar o projeto: 
  -  Entrar no diretório do manage.py (cd PagueBem_ML\manage.py)
  -  manage.py runserver

