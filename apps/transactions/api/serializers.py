from rest_framework import serializers

from apps.transactions.models import Transaction


class TransactionSerializerCreate(serializers.ModelSerializer):
    cpf = serializers.CharField(required=False)

    class Meta:
        model = Transaction
        fields = ('id', 'value', 'transaction_type', 'cpf')


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
