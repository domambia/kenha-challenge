"""
Response coordination URLs
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    IncidentAssignmentViewSet, ResponseMilestoneViewSet,
    ResponderLocationViewSet, ResponderChecklistViewSet,
)

app_name = 'response'

router = DefaultRouter()
router.register(r'assignments', IncidentAssignmentViewSet, basename='assignment')
router.register(r'milestones', ResponseMilestoneViewSet, basename='milestone')
router.register(r'locations', ResponderLocationViewSet, basename='location')
router.register(r'checklists', ResponderChecklistViewSet, basename='checklist')

urlpatterns = [
    path('', include(router.urls)),
]
