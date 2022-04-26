from typing import Union

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.carrier.api.serializers import CarrierSerializer
from apps.carrier.api.validators.cpf_validator import CpfValidator
from apps.carrier.models import Carrier


class CarrierViewSet(ViewSet):

    def create(self, request) -> Response:
        serializer = CarrierSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        carrier = Carrier.objects.create(
            name=data['name'],
            cpf=data['cpf']
        )

        carrier_s = CarrierSerializer(data=carrier)

        print(carrier_s.error_messages)

        return Response('Portador criado com sucesso', status=status.HTTP_201_CREATED)

    def destroy(self, request, pk: Union[int, None] = None) -> Response:
        Carrier.objects.get(pk=1).delete()
        return Response('Portador deletado com sucesso', status=status.HTTP_204_NO_CONTENT)
