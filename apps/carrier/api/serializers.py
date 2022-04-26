from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.carrier.models import Carrier
from .validators.cpf_validator import CpfValidator


class CarrierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrier
        fields = '__all__'
        extra_kwargs = {
            'cpf': {
                'validators': [
                    UniqueValidator(
                        queryset=Carrier.objects.all(),
                        message='CPF já cadastrado'
                    ),
                ]
            }
        }
