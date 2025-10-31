"""
Blockchain URLs
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlockchainTransactionViewSet

app_name = 'blockchain'

router = DefaultRouter()
router.register(r'transactions', BlockchainTransactionViewSet, basename='blockchain-transaction')

urlpatterns = [
    path('', include(router.urls)),
    path('incidents/<str:incident_id>/notarize/', 
         BlockchainTransactionViewSet.as_view({'post': 'notarize_incident'}),
         name='notarize-incident'),
]
