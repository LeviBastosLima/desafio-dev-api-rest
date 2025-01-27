from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from apps.carrier.models import Carrier


class CarrierTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        Carrier.objects.create(
            name='Maria',
            cpf='01205005072'
        )

    def setUp(self) -> None:
        self.client = APIClient()
        self.base_url = reverse('carriers-list')
        self.carrier_maria = Carrier.objects.get(cpf='01205005072')

    def test_create_carrier_successful(self) -> None:
        payload = {
            'name': 'Lucas da Silva',
            'cpf': '51153409097'
        }

        response = self.client.post(self.base_url, payload, format='json')

        actual_status_code = response.status_code
        expected_status_code = status.HTTP_201_CREATED

        created = Carrier.objects.filter(
            name=payload['name'],
            cpf=payload['cpf']
        ).exists()

        actual_response_data = response.data
        expected_response_data = {
            'message': 'Portador criado com sucesso'
        }

        self.assertTrue(created)
        self.assertEqual(expected_status_code, actual_status_code)
        self.assertEqual(expected_response_data, actual_response_data)

    def test_create_carrier_with_serializer_error(self):
        payload = {
            'cpf': '51153409097'
        }

        response = self.client.post(self.base_url, payload, format='json')

        actual_status_code = response.status_code
        expected_status_code = status.HTTP_400_BAD_REQUEST

        self.assertEqual(expected_status_code, actual_status_code)

    def test_create_carrier_with_cpf_unique_error(self):
        payload = {
            'name': 'Maria',
            'cpf': '01205005072'
        }

        response = self.client.post(self.base_url, payload, format='json')
        actual_status_code = response.status_code

        expected_status_code = status.HTTP_400_BAD_REQUEST

        self.assertEqual(expected_status_code, actual_status_code)

    def test_create_carrier_with_invalid_cpf(self) -> None:
        payload = {
            'name': 'Lucas da Silva',
            'cpf': '11111111111'
        }

        response = self.client.post(self.base_url, payload, format='json')
        actual_status_code = response.status_code

        expected_status_code = status.HTTP_400_BAD_REQUEST

        self.assertEqual(expected_status_code, actual_status_code)

    def test_delete_carrier_successful(self) -> None:
        url = f'{self.base_url}{self.carrier_maria.pk}/'

        response = self.client.delete(url)

        actual_status_code = response.status_code
        expected_status_code = status.HTTP_204_NO_CONTENT

        carrier = Carrier.objects.filter(pk=self.carrier_maria.pk).exists()

        self.assertFalse(carrier)
        self.assertEqual(expected_status_code, actual_status_code)

    def test_delete_carrier_error(self):
        url = f'{self.base_url}5/'

        response = self.client.delete(url)

        actual_status_code = response.status_code
        expected_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        carrier = Carrier.objects.filter(pk=self.carrier_maria.pk).exists()

        self.assertTrue(carrier)
        self.assertEqual(expected_status_code, actual_status_code)
