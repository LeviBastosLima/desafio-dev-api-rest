from django.db import models

from apps.digital_account.models import DigitalAccount


class Transaction(models.Model):
    class TransactionType(models.IntegerChoices):
        DEPOSIT = 0, 'Deposito'
        WITHDRAW = 1, 'Saque'

    value = models.DecimalField('Valor', decimal_places=2, max_digits=12)
    date_transaction = models.DateTimeField('Data da transação')
    transaction_type = models.IntegerField('Tipo da transação', choices=TransactionType.choices,
                                           default=TransactionType.DEPOSIT)

    digital_account = models.ForeignKey(DigitalAccount, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.transaction_type} de {self.value} reais - {self.date_transaction}'
