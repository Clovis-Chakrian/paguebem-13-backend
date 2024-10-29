from django.db import models

# Create your models here.

class Devedor(models.Model):
    devedor_id = models.AutoField(primary_key=True)  # Usar AutoField para chave primária
    indice_reputacao = models.DecimalField(max_digits=10, decimal_places=2)
    lead = models.IntegerField()

    def __str__(self):
        return f'Devedor {self.devedor_id} - Índice: {self.indice_reputacao}'