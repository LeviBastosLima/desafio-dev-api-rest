from django.db import models

from apps.carrier.models import Carrier


class DigitalAccount(models.Model):
    balance = models.DecimalField('Saldo', decimal_places=2, max_digits=12, default=0)
    number = models.CharField('Número da conta', max_length=9)
    agency = models.CharField('Agência', max_length=5)

    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE)

    def __str__(self):
        return f'Agência {self.agency} / Número da conta {self.number}'
