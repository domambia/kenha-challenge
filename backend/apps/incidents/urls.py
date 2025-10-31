"""
Incident URLs
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IncidentViewSet, IncidentCommentViewSet

app_name = 'incidents'

router = DefaultRouter()
router.register(r'', IncidentViewSet, basename='incident')
router.register(r'comments', IncidentCommentViewSet, basename='incident-comment')

urlpatterns = [
    path('', include(router.urls)),
]
