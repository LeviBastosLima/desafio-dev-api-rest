from datetime import datetime

from django.db.models import Sum
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.transactions.api.serializers import TransactionSerializer, TransactionSerializerCreate
from apps.transactions.models import Transaction
from apps.digital_account.models import DigitalAccount


class TransactionViewSet(ViewSet):

    def create(self, request):
        serializer = TransactionSerializerCreate(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        digital_account = DigitalAccount.objects.get(pk=data['digital_account_id'])

        if Transaction.TransactionType.WITHDRAW == data['transaction_type']:
            start_today = datetime.today().replace(hour=0, minute=0, second=0)
            end_today = datetime.today().replace(hour=23, minute=59, second=59)

            transaction = Transaction.objects.filter(digital_account_id=digital_account.pk,
                                                      date_transaction__gte=start_today,
                                                      date_transaction__lte=end_today).aggregate(Sum('value'))

            max_daily_withdraw = 2000.00
            total_transacion_value = transaction['value__sum'] + data['value']
            if total_transacion_value < max_daily_withdraw:
                if digital_account.balance > data['value']:
                    data['value'] = -data['value']
                else:
                    error_message = 'Error: Sua conta não possui saldo suficiente.'
                    raise PermissionDenied(error_message)
            else:
                error_message = 'Error: Seu limite de saque diário já foi utilizado.'
                raise PermissionDenied(error_message)

        digital_account.balance += data['value']
        print(digital_account.balance)
        digital_account.save()

        transaction = Transaction.objects.create(
            value=data['value'],
            date_transaction=datetime.now(),
            transaction_type=data['transaction_type'],
            digital_account=digital_account,
        )

        response_data = TransactionSerializer(transaction).data

        return Response({'message': 'Criado com sucesso', 'data': response_data}, status=status.HTTP_201_CREATED)

    def list(self, request):
        query = request.query_params

        start_date = query.get('start_date', datetime(2000, 1, 1))
        end_date = query.get('end_date', datetime(2050, 1, 1))
        digital_account_id = query.get('digital_account')

        transactions = Transaction.objects.filter(digital_account_id=digital_account_id,
                                                  date_transaction__gte=start_date,
                                                  date_transaction__lte=end_date)
        data = TransactionSerializer(transactions, many=True).data

        return Response(data)
