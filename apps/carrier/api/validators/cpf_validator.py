from rest_framework import serializers


class CpfValidator:
    def __call__(self, cpf):
        cpf_validated = True

        if len(cpf) != 11:
            cpf_validated = False

        if cpf == cpf[::-1]:
            cpf_validated = False

        for i in range(9, 11):
            value = sum((int(cpf[num]) * ((i + 1) - num) for num in range(0, i)))
            digit = ((value * 10) % 11) % 10
            if digit != int(cpf[i]):
                cpf_validated = False

        if not cpf_validated:
            message = 'CPF inválido'
            raise serializers.ValidationError(message, code='CPF')
