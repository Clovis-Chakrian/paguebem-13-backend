from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class Devedor(models.Model):
    devedor_id = models.AutoField(primary_key=True)  # Usar AutoField para chave primária
    indice_reputacao = models.DecimalField(max_digits=10, decimal_places=2)
    lead = models.IntegerField()

    def __str__(self):
        return f'Devedor {self.devedor_id} - Índice: {self.indice_reputacao}'

#---------------------------Usuário (Credores) ---------------------------------------
class CredorManager(BaseUserManager):
    def create_user(self, cnpj, razao_social, nome_fantasia, email, password=None):
        if not email:
            raise ValueError("Usuários devem ter um endereço de email")

        user = self.model(
            cnpj=cnpj,
            razao_social=razao_social,
            nome_fantasia=nome_fantasia,
            email=self.normalize_email(email),
        )
        user.set_password(password)  # Criptografa a senha
        user.save(using=self._db)
        return user

class Credor(AbstractBaseUser):
    credor_id = models.AutoField(primary_key=True)  # Automaticamente gerado
    cnpj = models.CharField(max_length=18, unique=True)
    razao_social = models.CharField(max_length=255)
    nome_fantasia = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # pode usar `set_password` para criptografar

    is_active = models.BooleanField(default=True)

    objects = CredorManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['cnpj', 'razao_social', 'nome_fantasia']

    def __str__(self):
        return self.email
#---------------------------Fim Usuário---------------------------------------

class Conta(models.Model):
    conta_id = models.AutoField(primary_key=True)
    devedor = models.ForeignKey(Devedor, on_delete=models.CASCADE)
    credor = models.ForeignKey(Credor, on_delete=models.CASCADE)
    valor_total = models.DecimalField(max_digits=30, decimal_places=2)
    numero_parcelas = models.IntegerField()

    def _str_(self):
        return f'Conta {self.conta_id} - Valor Total: {self.valor_total}'


class Pagamento(models.Model):
    pagamento_id = models.AutoField(primary_key=True)
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE)
    numero_parcela = models.IntegerField()
    numero_documento = models.IntegerField()
    vencimento = models.DateField()
    data_pagamento = models.DateField(null=True, blank=True)
    tempo_para_pagar = models.IntegerField()
    valor_pagamento = models.DecimalField(max_digits=30, decimal_places=2)
    valor_pago = models.DecimalField(max_digits=30, decimal_places=2)
    diferenca_valores = models.DecimalField(max_digits=30, decimal_places=2)
    lead = models.IntegerField()

    def _str_(self):
        return f'Pagamento {self.pagamento_id} - Parcela: {self.numero_parcela}'
