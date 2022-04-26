from django.db import models


class Carrier(models.Model):
    name = models.CharField('Nome completo', max_length=130)
    cpf = models.CharField('CPF', max_length=11, unique=True)

    def __str__(self):
        return self.name
