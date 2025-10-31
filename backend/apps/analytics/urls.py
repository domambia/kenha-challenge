"""
Analytics URLs
"""
from django.urls import path
from .views import (
    AnalyticsDashboardView, IncidentHeatmapView,
    TrafficFlowView, WeatherConditionsView, RoadConditionsView
)

app_name = 'analytics'

urlpatterns = [
    path('dashboard/', AnalyticsDashboardView.as_view(), name='dashboard'),
    path('heatmap/', IncidentHeatmapView.as_view(), name='heatmap'),
    path('traffic-flow/', TrafficFlowView.as_view(), name='traffic-flow'),
    path('weather/', WeatherConditionsView.as_view(), name='weather'),
    path('road-conditions/', RoadConditionsView.as_view(), name='road-conditions'),
]
