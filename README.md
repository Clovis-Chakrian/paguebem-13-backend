
---

# 🌟 **Backend PagueBem - Squad 13**  
**Residência em Tecnologia 2024.2**  

![Python](https://img.shields.io/badge/Python-3.12.1-blue?logo=python&logoColor=white)  
![Django](https://img.shields.io/badge/Django-4.2.6-success?logo=django&logoColor=white)  
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-v15-blue?logo=postgresql&logoColor=white)  

Este repositório contém o código-fonte do backend desenvolvido pela **Squad 13** para o projeto **PagueBem**, uma solução tecnológica para gerenciamento de cobranças e combate à inadimplência.  

## 🚀 **Tecnologias Utilizadas**  
O projeto foi construído com as seguintes ferramentas e bibliotecas:  

- **Django Framework**: Estrutura robusta para o desenvolvimento backend.  
- **Django REST Framework (DRF)**: Criação e gerenciamento de APIs RESTful.  
- **Django REST Framework SimpleJWT**: Autenticação baseada em tokens JWT.  
- **Swagger (drf_yasg)**: Documentação interativa e visual das APIs.  
- **CORS Headers**: Configuração para acesso de domínios externos ao backend.  

---

## ⚙️ **Configuração do Projeto**  
Siga o passo a passo abaixo para configurar e executar o projeto localmente:  

### 1️⃣ **Clonar o Repositório**  
Primeiro, clone o repositório em sua máquina local:  
```bash
git clone https://github.com/Clovis-Chakrian/paguebem-13-backend.git
cd paguebem-13-backend
```

---

### 2️⃣ **Pré-requisitos**  
Certifique-se de ter instaladas as seguintes ferramentas:  
- Python 3.12.1 (baixe [aqui](https://www.python.org/downloads/))  
- PostgreSQL (configurado com as credenciais do projeto)  

---

### 3️⃣ **Configurar Ambiente Virtual**  
1. **Remova qualquer ambiente existente**:  
   Apague a pasta `.venv`, se houver.  

2. **Crie um novo ambiente virtual**:  
   ```bash
   python -m venv ./env
   ```  

3. **Ative o ambiente virtual**:  
   - **Windows**:  
     ```bash
     .\env\Scripts\activate
     ```  
   - **macOS/Linux**:  
     ```bash
     source env/bin/activate
     ```  

---

### 4️⃣ **Instalar Dependências**  
Com o ambiente virtual ativado, instale as dependências do projeto:  
```bash
pip install -r requirements.txt
```  

---

### 5️⃣ **Configurar o Banco de Dados**  
No arquivo de configuração `PagueBem_ML/settings.py`, configure as credenciais do PostgreSQL:  

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

### 6️⃣ **Preparar o Banco de Dados**  
1. Navegue até o diretório do projeto:  
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

---

### 7️⃣ **Executar o Servidor**  
Para iniciar o servidor local, rode:  
```bash
python manage.py runserver
```  

💻 **O backend estará disponível no navegador em:**  
[http://127.0.0.1:8000](http://127.0.0.1:8000)  

---

## 📁 **Estrutura do Repositório**  

```plaintext
PagueBem_ML/
├── pagamentos/            # Aplicação principal
├── PagueBem_ML/           # Configurações do projeto Django
├── requirements.txt       # Dependências do projeto
└── manage.py              # Script principal do Django
```

---

## 📜 **Documentação da API**  
Acesse a documentação interativa gerada automaticamente com Swagger em:  
[http://127.0.0.1:8000/swagger](http://127.0.0.1:8000/swagger)  

---

## 🎯 **Contribuição**  
Caso queira contribuir, siga as diretrizes do repositório e envie um pull request!  

---

## 📞 **Contato**  
Entre em contato com a **Squad 13** em caso de dúvidas ou sugestões:  
- GitHub: [Repositório Oficial](https://github.com/Clovis-Chakrian/paguebem-13-backend.git)  

✨ **Obrigado por visitar nosso projeto!**  
