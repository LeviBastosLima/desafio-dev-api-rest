from rest_framework import serializers

from apps.transactions.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    cpf = serializers.CharField(required=False)

    class Meta:
        model = Transaction
        fields = ('id', 'value', 'transaction_type', 'cpf')
