
---

# Backend PagueBem Squad 13 
**Residência 2024.2**

Este repositório contém o código-fonte do backend desenvolvido pela Squad 13 para o projeto PagueBem, criado como parte da Residência em Tecnologia.

## Requisitos
- **Python**: 3.12.1
- **PostgreSQL**: Configurado com as credenciais do projeto

## Configuração do Projeto
Siga os passos abaixo para configurar e executar o projeto localmente.

### Passo 1: Instalar Python
Certifique-se de que o Python 3.12.1 esteja instalado em sua máquina. Você pode fazer o download [aqui](https://www.python.org/downloads/).

### Passo 2: Configurar Ambiente Virtual
1. Remova o ambiente virtual existente, caso exista, apagando a pasta `.venv`.
2. Crie um novo ambiente virtual com o comando:
   ```bash
   python -m venv ./env
   ```
3. Ative o ambiente virtual:
   - **Windows**:
     ```bash
     .\env\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source env/bin/activate
     ```

### Passo 3: Instalar Dependências
Instale todas as dependências do projeto:
```bash
pip install -r requirements.txt
```

### Passo 4: Configurar o Banco de Dados
No arquivo de configuração `PagueBem_ML/settings.py`, configure o banco de dados PostgreSQL com as credenciais e detalhes do ambiente:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': ' ',
        'PASSWORD': ' ',
        'HOST': ' ', 
        'PORT': ' ', 
    }
```

### Passo 5: Inicializar o Banco de Dados
1. Acesse o diretório onde está o arquivo `manage.py`:
   ```bash
   cd PagueBem_ML
   ```
2. Crie as migrações necessárias:
   ```bash
   python manage.py makemigrations
   ```
3. Aplique as migrações ao banco de dados:
   ```bash
   python manage.py migrate
   ```

### Passo 6: Executar o Servidor
Inicie o servidor Django localmente:
```bash
python manage.py runserver
```

### Pronto! 🎉
Agora o backend está rodando localmente em `http://127.0.0.1:8000/`.

## Estrutura do Repositório
- `PagueBem_ML/`: Contém a configuração do Django e os arquivos do projeto.
- `requirements.txt`: Lista de dependências do Python necessárias para rodar o projeto.
- `.venv/`: Diretório gerado para o ambiente virtual (não incluído no repositório).

## Contato
Em caso de dúvidas ou sugestões, entre em contato com a Squad 13 da PagueBem.

--- 
