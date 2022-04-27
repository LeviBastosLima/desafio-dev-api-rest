from datetime import datetime

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

        digital_account = DigitalAccount.objects.create(
            balance=5500.00,
            agency='0003',
            number='56813658',
            carrier=carrier
        )

        Transaction.objects.create(
            value=3000.00,
            date_transaction=datetime(2022, 4, 23, 18, 20, 55),
            digital_account=digital_account
        )

        Transaction.objects.create(
            value=3500.00,
            date_transaction=datetime(2022, 4, 25, 16, 56, 23),
            digital_account=digital_account
        )

        Transaction.objects.create(
            value=1000.00,
            date_transaction=datetime(2022, 4, 27, 12, 1, 25),
            transaction_type=Transaction.TransactionType.WITHDRAW,
            digital_account=digital_account
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
            'digital_account_id': self.digital_account.pk
        }

        response = self.client.post(self.base_url, payload, format='json')

        actual_status_code = response.status_code
        expected_status_code = status.HTTP_201_CREATED
        created = Transaction.objects.filter(
            pk=response.data['data']['id'],
        ).exists()

        actual_balance = DigitalAccount.objects.get(pk=payload['digital_account_id']).balance
        expected_balance = 6500.00

        self.assertEqual(actual_status_code, expected_status_code)
        self.assertEqual(actual_balance, expected_balance)
        self.assertTrue(created)

    def test_withdraw_successful(self):
        payload = {
            'value': 1000,
            'transaction_type': 1,
            'digital_account_id': self.digital_account.pk
        }

        response = self.client.post(self.base_url, payload, format='json')

        actual_status_code = response.status_code
        expected_status_code = status.HTTP_201_CREATED
        created = Transaction.objects.filter(
            pk=response.data['data']['id'],
        ).exists()

        actual_balance = DigitalAccount.objects.get(pk=payload['digital_account_id']).balance
        expected_balance = 4500.00

        self.assertEqual(actual_status_code, expected_status_code)
        self.assertEqual(actual_balance, expected_balance)
        self.assertTrue(created)

    def test_withdraw_over_balance(self):
        payload = {
            'value': 10000,
            'transaction_type': 1,
            'digital_account_id': self.digital_account.pk
        }

        response = self.client.post(self.base_url, payload, format='json')
        actual_status_code = response.status_code
        expected_status_code = status.HTTP_403_FORBIDDEN

        self.assertEqual(actual_status_code, expected_status_code)

    def test_withdraw_over_daily_limit(self):
        payload = {
            'value': 1500,
            'transaction_type': 1,
            'digital_account_id': self.digital_account.pk
        }

        response = self.client.post(self.base_url, payload, format='json')
        actual_status_code = response.status_code
        expected_status_code = status.HTTP_403_FORBIDDEN

        print(response.data)

        self.assertEqual(expected_status_code, actual_status_code)

    def test_get_extract(self):
        response = self.client.get(f'{self.base_url}?digital_account={self.digital_account.pk}', )

        actual_status_code = response.status_code
        expected_status_code = 200

        actual_number_of_results = len(response.data)
        expected_number_of_results = 3

        self.assertEqual(expected_status_code, actual_status_code)
        self.assertEqual(expected_number_of_results, actual_number_of_results)

    def test_get_extract_with_period(self):
        start_date = '2022-04-25'
        end_date = '2022-04-27'
        params = f'start_date={start_date}&end_date={end_date}&digital_account={self.digital_account.pk}'

        response = self.client.get(f'{self.base_url}?{params}', HTTP_CARRIER=self.carrier_lucas.pk)

        actual_status_code = response.status_code
        expected_status_code = 200

        actual_number_of_results = len(response.data)
        expected_number_of_results = 2

        self.assertEqual(expected_status_code, actual_status_code)
        self.assertEqual(expected_number_of_results, actual_number_of_results)
