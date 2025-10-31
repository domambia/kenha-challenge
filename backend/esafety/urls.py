"""
eSafety URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),
    # JWT token endpoints - handled by simplejwt
    path('api/incidents/', include('apps.incidents.urls')),
    path('api/media/', include('apps.media.urls')),
    path('api/response/', include('apps.response.urls')),
    path('api/iot/', include('apps.iot.urls')),
    path('api/verification/', include('apps.verification.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
    path('api/blockchain/', include('apps.blockchain.urls')),
    path('api/config/', include('apps.config.urls')),
    path('api/work-orders/', include('apps.workorders.urls')),
    path('api/audit/', include('apps.audit.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

