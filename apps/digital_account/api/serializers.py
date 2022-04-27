from rest_framework import serializers

from apps.carrier.api.serializers import CarrierSerializer
from apps.digital_account.models import DigitalAccount
from apps.validators.cpf_validator import CpfValidator


class DigitalAccountSerializerCreate(serializers.ModelSerializer):
    cpf = serializers.CharField()

    class Meta:
        model = DigitalAccount
        fields = ('agency', 'number', 'cpf')
        extra_kwargs = {
            'cpf': {
                'validators': [
                    CpfValidator()
                ]
            }
        }


class DigitalAccountSerializerStatusActive(serializers.ModelSerializer):
    class Meta:
        model = DigitalAccount
        fields = ('active',)


class DigitalAccountSerializer(serializers.ModelSerializer):

    carrier = CarrierSerializer(read_only=True, required=False)

    class Meta:
        model = DigitalAccount
        fields = ('agency', 'number', 'balance', 'carrier')

