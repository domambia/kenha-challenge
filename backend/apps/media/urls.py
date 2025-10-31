from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MediaAssetViewSet

app_name = 'media'

router = DefaultRouter()
router.register(r'', MediaAssetViewSet, basename='media')

urlpatterns = [
    path('', include(router.urls)),
]
