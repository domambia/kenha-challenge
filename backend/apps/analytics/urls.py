"""
Analytics URLs
"""
from django.urls import path
from .views import AnalyticsDashboardView, IncidentHeatmapView

app_name = 'analytics'

urlpatterns = [
    path('dashboard/', AnalyticsDashboardView.as_view(), name='dashboard'),
    path('heatmap/', IncidentHeatmapView.as_view(), name='heatmap'),
]
