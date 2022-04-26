from rest_framework import serializers


class CpfValidator:
    def __int__(self):
        self.cpf_valid = True

    def __call__(self, cpf):
        if len(cpf) != 11:
            self.cpf_valid = False

        #  Verifica se o CPF tem todos os números iguais, ex: 111.111.111-11
        if cpf == cpf[::-1]:
            self.cpf_valid = False

        #  Valida os dois dígitos verificadores
        for i in range(9, 11):
            value = sum((int(cpf[num]) * ((i + 1) - num) for num in range(0, i)))
            digit = ((value * 10) % 11) % 10
            if digit != cpf[i]:
                self.cpf_valid = False

        if not self.cpf_valid:
            message = 'CPF inválido'
            raise serializers.ValidationError(message, code='CPF')
