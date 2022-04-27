from rest_framework import serializers

from apps.transactions.models import Transaction
from apps.validators.cpf_validator import CpfValidator


class TransactionSerializerCreate(serializers.ModelSerializer):
    cpf = serializers.CharField(required=False)

    class Meta:
        model = Transaction
        fields = ('id', 'value', 'transaction_type', 'cpf')
        extra_kwargs = {
            'cpf': {
                'validators': [
                    CpfValidator()
                ]
            }
        }


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
