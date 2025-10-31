"""
IoT integration URLs
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RFIDReaderViewSet, RFIDLogViewSet,
    CCTVCameraViewSet, CCTVFeedViewSet,
    SensorViewSet, SensorReadingViewSet,
    IncidentValidationViewSet,
)

app_name = 'iot'

router = DefaultRouter()
router.register(r'rfid/readers', RFIDReaderViewSet, basename='rfid-reader')
router.register(r'rfid/logs', RFIDLogViewSet, basename='rfid-log')
router.register(r'cctv/cameras', CCTVCameraViewSet, basename='cctv-camera')
router.register(r'cctv/feeds', CCTVFeedViewSet, basename='cctv-feed')
router.register(r'sensors', SensorViewSet, basename='sensor')
router.register(r'sensors/readings', SensorReadingViewSet, basename='sensor-reading')
router.register(r'validation', IncidentValidationViewSet, basename='incident-validation')

urlpatterns = [
    path('', include(router.urls)),
    path('validation/incidents/<str:incident_id>/', 
         IncidentValidationViewSet.as_view({'post': 'validate_incident'}), 
         name='validate-incident'),
]
