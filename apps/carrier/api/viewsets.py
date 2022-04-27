from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.carrier.api.serializers import CarrierSerializer
from apps.carrier.models import Carrier


class CarrierViewSet(ViewSet):

    def create(self, request) -> Response:
        serializer = CarrierSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        Carrier.objects.create(
            name=data['name'],
            cpf=data['cpf']
        )

        return Response({'message': 'Portador criado com sucesso'}, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk: int) -> Response:
        try:
            Carrier.objects.get(pk=pk).delete()
            return Response('Portador deletado com sucesso', status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(f'Error>>> {e}')
            raise APIException()
