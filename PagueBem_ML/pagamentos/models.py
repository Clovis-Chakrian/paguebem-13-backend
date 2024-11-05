from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class TipoPessoa(models.TextChoices):
    PESSOA_JURIDICA = 'PJ', _('Pessoa Jurídica')
    PESSOA_FISICA = 'PF', _('Pessoa Física')

# Modelo de Devedor com validação de PJ/PF
class Devedor(models.Model):
    devedor_id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=2, choices=TipoPessoa.choices, default=TipoPessoa.PESSOA_FISICA)
    
    # Campos para PF
    cpf = models.CharField(max_length=11, blank=True, null=True)
    nome = models.CharField(max_length=255, blank=True, null=True)
    
    # Campos para PJ
    cnpj = models.CharField(max_length=18, blank=True, null=True)
    razao_social = models.CharField(max_length=255, blank=True, null=True)
    nome_fantasia = models.CharField(max_length=255, blank=True, null=True)
    
    email = models.EmailField(unique=True)
    celular = models.CharField(max_length=15, blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    indice_reputacao = models.DecimalField(max_digits=10, decimal_places=2)
    lead = models.IntegerField()

    def clean(self):
        if self.tipo == TipoPessoa.PESSOA_FISICA:
            # Validação para Pessoa Física
            if not self.cpf or not self.nome:
                raise ValidationError("CPF e Nome são obrigatórios para Pessoa Física.")
            # Limpar campos exclusivos de PJ
            self.cnpj = None
            self.razao_social = None
            self.nome_fantasia = None

        elif self.tipo == TipoPessoa.PESSOA_JURIDICA:
            # Validação para Pessoa Jurídica
            if not self.cnpj or not self.razao_social or not self.nome_fantasia:
                raise ValidationError("CNPJ, Razão Social e Nome Fantasia são obrigatórios para Pessoa Jurídica.")
            # Limpar campos exclusivos de PF
            self.cpf = None
            self.nome = None

    def save(self, *args, **kwargs):
        self.clean()  # Chama a validação antes de salvar
        super().save(*args, **kwargs)  # Salva o objeto se tudo estiver válido

    def __str__(self):
        return f'Devedor {self.devedor_id} - Índice: {self.indice_reputacao}'

class CredorManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O campo email é obrigatório")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
# Modelo de Credor com validação de PJ/PF
class Credor(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=2, choices=TipoPessoa.choices, default=TipoPessoa.PESSOA_JURIDICA)
    
    # Campos para PF
    cpf = models.CharField(max_length=11, blank=True, null=True)
    nome = models.CharField(max_length=255, blank=True, null=True)
    
    # Campos para PJ
    cnpj = models.CharField(max_length=18, blank=True, null=True)
    razao_social = models.CharField(max_length=255, blank=True, null=True)
    nome_fantasia = models.CharField(max_length=255, blank=True, null=True)
    
    email = models.EmailField(unique=True)
    celular = models.CharField(max_length=15, blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    objects = CredorManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def clean(self):
        if self.tipo == TipoPessoa.PESSOA_FISICA:
            # Validação para Pessoa Física
            if not self.cpf or not self.nome:
                raise ValidationError("CPF e Nome são obrigatórios para Pessoa Física.")
            # Limpar campos exclusivos de PJ
            self.cnpj = None
            self.razao_social = None
            self.nome_fantasia = None

        elif self.tipo == TipoPessoa.PESSOA_JURIDICA:
            # Validação para Pessoa Jurídica
            if not self.cnpj or not self.razao_social or not self.nome_fantasia:
                raise ValidationError("CNPJ, Razão Social e Nome Fantasia são obrigatórios para Pessoa Jurídica.")
            # Limpar campos exclusivos de PF
            self.cpf = None
            self.nome = None

    def save(self, *args, **kwargs):
        self.clean()  # Chama a validação antes de salvar
        super().save(*args, **kwargs)  # Salva o objeto se tudo estiver válido

    def __str__(self):
        return self.email

class Conta(models.Model):
    conta_id = models.AutoField(primary_key=True)
    devedor = models.ForeignKey(Devedor, on_delete=models.CASCADE)
    credor = models.ForeignKey(Credor, on_delete=models.CASCADE)
    valor_total = models.DecimalField(max_digits=30, decimal_places=2)
    numero_parcelas = models.IntegerField()

    def __str__(self):
        return f'Conta {self.conta_id} - Valor Total: {self.valor_total}'

# Modelo de Pagamento
class Pagamento(models.Model):
    pagamento_id = models.AutoField(primary_key=True)
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE)
    
    # Novas chaves estrangeiras para acesso direto ao credor e devedor
    devedor = models.ForeignKey(Devedor, on_delete=models.CASCADE)
    credor = models.ForeignKey(Credor, on_delete=models.CASCADE)
    
    numero_parcela = models.IntegerField()
    numero_documento = models.IntegerField()
    vencimento = models.DateField()
    data_pagamento = models.DateField(null=True, blank=True)
    tempo_para_pagar = models.IntegerField()
    valor_pagamento = models.DecimalField(max_digits=30, decimal_places=2)
    valor_pago = models.DecimalField(max_digits=30, decimal_places=2)
    diferenca_valores = models.DecimalField(max_digits=30, decimal_places=2)
    lead = models.IntegerField()

    def __str__(self):
        return f'Pagamento {self.pagamento_id} - Parcela: {self.numero_parcela}'