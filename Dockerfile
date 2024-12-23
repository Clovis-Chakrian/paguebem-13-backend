FROM python:3.10

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    apt-get clean

# Configurar o ambiente
WORKDIR /app
COPY requirements.txt .

# Instalar dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "PagueBem_ML/manage.py", "runserver", "0.0.0.0:8000"]
