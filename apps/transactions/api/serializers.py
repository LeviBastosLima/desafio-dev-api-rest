from rest_framework import serializers

from apps.transactions.models import Transaction
from apps.validators.cpf_validator import CpfValidator


class TransactionSerializerCreate(serializers.ModelSerializer):
    digital_account_id = serializers.CharField()

    class Meta:
        model = Transaction
        fields = ('id', 'value', 'transaction_type', 'digital_account_id')


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
