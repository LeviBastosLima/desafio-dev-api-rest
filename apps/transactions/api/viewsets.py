from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.transactions.api.serializers import TransactionSerializer
from apps.transactions.models import Transaction
from apps.digital_account.models import DigitalAccount


class TransactionViewSet(ViewSet):

    def create(self, request):
        serializer = TransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        digital_account = DigitalAccount.objects.get(carrier__cpf=data['cpf'])
        data['value'] = data['value'] if data['transaction_type'] == Transaction.TransactionType.DEPOSIT \
            else -data['value']
        digital_account.balance += data['value']

        if digital_account.balance < 0:
            value_withdraw = -data['value']
            raise f"Error, Sua conta possui {digital_account.balance + value_withdraw} " \
                  f"e você está tentando sacar {value_withdraw}"

        digital_account.save()

        transaction = Transaction.objects.create(
            value=data['value'],
            date_transaction=datetime.now(),
            transaction_type=data['transaction_type'],
            digital_account=digital_account,
        )

        response_data = TransactionSerializer(transaction).data

        return Response({'message': 'Criado com sucesso', 'data': response_data}, status=status.HTTP_201_CREATED)
