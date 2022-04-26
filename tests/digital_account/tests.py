from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from apps.carrier.models import Carrier
from apps.digital_account.models import DigitalAccount


class DigitalAccountTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Carrier.objects.create(
            name='Maria',
            cpf='01205005072'
        )

        carrier = Carrier.objects.create(
            name='Junior',
            cpf='86902396000'
        )

        DigitalAccount.objects.create(
            agency='0003',
            number='56813658',
            carrier=carrier
        )

    def setUp(self) -> None:
        self.client = APIClient()
        self.base_url = reverse('digital-accounts-list')
        self.carrier_maria = Carrier.objects.get(cpf='01205005072')
        self.carrier_Junior = Carrier.objects.get(cpf='86902396000')
        self.digital_account = DigitalAccount.objects.get(agency='0003', number='56813658', carrier=self.carrier_Junior)

    def test_create_digital_account_successful(self):
        payload = {
            'cpf': self.carrier_maria.cpf,
            'agency': '0055',
            'number': '56895236'
        }

        response = self.client.post(self.base_url, payload, format='json')
        actual_status_code = response.status_code

        print(response.data)

        expected_status_code = status.HTTP_201_CREATED

        created = DigitalAccount.objects.filter(
            agency=payload['agency'],
            number=payload['number'],
            carrier=self.carrier_maria
        ).exists()

        self.assertEqual(expected_status_code, actual_status_code)
        self.assertTrue(created)

    def test_retrieve_digital_account_successful(self):

        response = self.client.get(f'{self.base_url}{self.digital_account.pk}/')

        actual_data = response.data
        expected_data = {'agency': '0003', 'number': '56813658', 'balance': '0.00'}

        self.assertEqual(expected_data, actual_data)

    def test_disable_digital_account(self):
        payload = {
            'active': False
        }
        self.client.patch(f'{self.base_url}{self.digital_account.pk}/', payload, format='json',
                          HTTP_CARRIER=self.carrier_Junior.pk)

        actual_active = DigitalAccount.objects.get(pk=self.digital_account.pk).active

        self.assertFalse(actual_active)

    def test_delete_digital_account_successful(self):
        response = self.client.delete(f'{self.base_url}{self.digital_account.pk}/', HTTP_CARRIER=self.carrier_Junior.pk)
        actual_status_code = response.status_code

        expected_status_code = status.HTTP_204_NO_CONTENT

        exist = DigitalAccount.objects.filter(carrier=self.carrier_Junior).exists()

        self.assertEqual(expected_status_code, actual_status_code)
        self.assertFalse(exist)
