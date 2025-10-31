"""
Work order URLs
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkOrderViewSet, InfrastructureInspectionViewSet

app_name = 'workorders'

router = DefaultRouter()
router.register(r'', WorkOrderViewSet, basename='work-order')
router.register(r'inspections', InfrastructureInspectionViewSet, basename='inspection')

urlpatterns = [
    path('', include(router.urls)),
]
