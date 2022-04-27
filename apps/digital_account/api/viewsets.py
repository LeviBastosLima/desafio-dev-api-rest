from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.carrier.models import Carrier
from .serializers import DigitalAccountSerializerCreate, DigitalAccountSerializer, DigitalAccountSerializerStatusActive
from apps.digital_account.models import DigitalAccount


class DigitalAccountViewSet(ViewSet):

    def create(self, request):

        serializer = DigitalAccountSerializerCreate(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        carrier = Carrier.objects.get(cpf=data['cpf'])

        DigitalAccount.objects.create(
            agency=data['agency'],
            number=data['number'],
            carrier=carrier
        )

        return Response({'message': 'Conta digital criada com sucesso'}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk):
        try:
            digital_account = DigitalAccountSerializer(DigitalAccount.objects.get(pk=pk)).data

            return Response({
                'agency': digital_account['agency'],
                'number': digital_account['number'],
                'balance': digital_account['balance']
            })
        except DigitalAccount.DoesNotExist as e:
            print(e)
            raise ValidationError('Conta digital não existe')
        except Exception as e:
            print(e)
            raise APIException()

    def partial_update(self, request, pk):
        serializer = DigitalAccountSerializerStatusActive(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        digital_account = DigitalAccount.objects.get(pk=pk)
        digital_account.active = data['active']
        digital_account.save()

        active_status = 'ativada' if data['active'] else 'desativada'
        return Response({'message': f'Conta digital {active_status} com sucesso'})

    def destroy(self, request, pk) -> Response:
        try:
            DigitalAccount.objects.get(pk=pk).delete()
            return Response({'message': 'Conta digital deletada com sucesso'}, status=status.HTTP_204_NO_CONTENT)
        except DigitalAccount.DoesNotExist as e:
            print(e)
            raise ValidationError('Conta digital não existe')
        except Exception as e:
            print(e)
            raise APIException()
