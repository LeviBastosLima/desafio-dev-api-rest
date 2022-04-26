from rest_framework import serializers

from apps.carrier.api.serializers import CarrierSerializer
from apps.digital_account.models import DigitalAccount


class DigitalAccountSerializerCreate(serializers.ModelSerializer):
    cpf = serializers.CharField()

    class Meta:
        model = DigitalAccount
        fields = ('agency', 'number', 'cpf')


class DigitalAccountSerializerStatusActive(serializers.ModelSerializer):
    class Meta:
        model = DigitalAccount
        fields = ('active',)


class DigitalAccountSerializer(serializers.ModelSerializer):

    carrier = CarrierSerializer(read_only=True, required=False)

    class Meta:
        model = DigitalAccount
        fields = ('agency', 'number', 'balance', 'carrier')

