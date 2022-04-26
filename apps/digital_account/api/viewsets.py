from django.core import serializers

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.carrier.models import Carrier
from .serializers import DigitalAccountSerializerCreate, DigitalAccountSerializer, DigitalAccountSerializerStatusActive
from apps.digital_account.models import DigitalAccount


class DigitalAccountViewSet(ViewSet):

    def create(self, request):

        serializer = DigitalAccountSerializerCreate(data=request.data)
        print(serializer)
        if not serializer.is_valid():
            return Response('Error', status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        carrier = Carrier.objects.get(cpf=data['cpf'])

        DigitalAccount.objects.create(
            agency=data['agency'],
            number=data['number'],
            carrier=carrier
        )

        return Response('Conta criada com sucesso', status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk):
        digital_account = DigitalAccountSerializer(DigitalAccount.objects.get(pk=pk)).data

        return Response({
            'agency': digital_account['agency'],
            'number': digital_account['number'],
            'balance': digital_account['balance']
        }, status=status.HTTP_200_OK)

    def partial_update(self, request, pk):
        serializer = DigitalAccountSerializerStatusActive(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        carrier_id = request.META['HTTP_CARRIER']

        digital_account = DigitalAccount.objects.get(pk=pk, carrier_id=carrier_id)
        digital_account.active = data['active']
        digital_account.save()

        active_status = 'ativada' if data['active'] else 'desativada'
        return Response(f'Conta digital {active_status} com sucesso')

    def destroy(self, request, pk) -> Response:
        carrier_id = request.META['HTTP_CARRIER']

        DigitalAccount.objects.get(pk=pk, carrier_id=carrier_id).delete()

        return Response('Conta digital deletada com sucesso', status=status.HTTP_204_NO_CONTENT)
