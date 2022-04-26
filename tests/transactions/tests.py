import datetime

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from apps.carrier.models import Carrier
from apps.digital_account.models import DigitalAccount
from apps.transactions.models import Transaction


class TransactionTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        carrier = Carrier.objects.create(
            name='Junior',
            cpf='86902396000'
        )

        DigitalAccount.objects.create(
            balance=5500.00,
            agency='0003',
            number='56813658',
            carrier=carrier
        )

    def setUp(self) -> None:
        self.client = APIClient()
        self.base_url = reverse('transactions-list')
        self.carrier_lucas = Carrier.objects.get(cpf='86902396000')
        self.digital_account = DigitalAccount.objects.get(agency='0003', number='56813658', carrier=self.carrier_lucas)

    def test_deposit_successful(self):
        payload = {
            'value': 1000,
            'transaction_type': 0,
            'cpf': '86902396000'
        }

        response = self.client.post(self.base_url, payload, format='json')

        actual_status_code = response.status_code
        expected_status_code = status.HTTP_201_CREATED
        created = Transaction.objects.filter(
            pk=response.data['data']['id'],
        ).exists()

        actual_balance = DigitalAccount.objects.get(carrier__cpf=payload['cpf']).balance
        expected_balance = 6500.00

        self.assertEqual(actual_status_code, expected_status_code)
        self.assertEqual(actual_balance, expected_balance)
        self.assertTrue(created)

    def test_withdraw_successful(self):
        payload = {
            'value': 1000,
            'transaction_type': 1,
            'cpf': '86902396000'
        }

        response = self.client.post(self.base_url, payload, format='json')

        actual_status_code = response.status_code
        expected_status_code = status.HTTP_201_CREATED
        created = Transaction.objects.filter(
            pk=response.data['data']['id'],
        ).exists()

        actual_balance = DigitalAccount.objects.get(carrier__cpf=payload['cpf']).balance
        expected_balance = 4500.00

        self.assertEqual(actual_status_code, expected_status_code)
        self.assertEqual(actual_balance, expected_balance)
        self.assertTrue(created)

    def test_withdraw_over_balance(self):
        payload = {
            'value': 10000,
            'transaction_type': 1,
            'cpf': '86902396000'
        }

        response = self.client.post(self.base_url, payload, format='json')

        print(response)

        actual_status_code = response.status_code
        expected_status_code = status.HTTP_201_CREATED
        created = Transaction.objects.filter(
            pk=response.data['data']['id'],
        ).exists()

        actual_balance = DigitalAccount.objects.get(carrier__cpf=payload['cpf']).balance
        expected_balance = 4500.00

        self.assertEqual(actual_status_code, expected_status_code)
        self.assertEqual(actual_balance, expected_balance)
        self.assertTrue(created)