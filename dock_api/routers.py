from rest_framework import routers

from apps.carrier.api.viewsets import CarrierViewSet
from apps.digital_account.api.viewsets import DigitalAccountViewSet
from apps.transactions.api.viewsets import TransactionViewSet

router = routers.SimpleRouter()

router.register(r'carriers', CarrierViewSet, basename='carriers')
router.register(r'digital-accounts', DigitalAccountViewSet, basename='digital-accounts')
router.register(r'transactions', TransactionViewSet, basename='transactions')

url_routers = router.urls
