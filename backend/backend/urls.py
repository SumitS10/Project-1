"""
URL configuration for backend project.
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from app.views import (
    UploadFidelityView,
    UploadTradierView,
    FidelityTradeListView,
    TradierTradeListView,
    ReactAppView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/upload-fidelity/', UploadFidelityView.as_view()),
    path('api/upload-tradier/', UploadTradierView.as_view()),
    path('api/fidelity-trades/', FidelityTradeListView.as_view()),
    path('api/tradier-trades/', TradierTradeListView.as_view()),
    
    # Serve static files from React build
    re_path(r'^assets/(?P<path>.*)$', serve, {'document_root': settings.FRONTEND_BUILD_DIR / 'assets'}),
    
    # Catch-all: serve React app (must be last)
    re_path(r'^.*$', ReactAppView.as_view()),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
