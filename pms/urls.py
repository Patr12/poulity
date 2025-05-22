from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('customers/', include('customers.urls')),
    path('staff/', include('staff.urls')),
    path('finance/', include('finance.urls')),
    # In your urls.py
path('production/', include('production.urls')),  # Make sure only one with this namespace

    path('health/', include('health.urls')),
    path('inventory/', include('inventory.urls')),
    path('reports/', include('reports.urls')),
    path('documents/', include('documents.urls')),
]

# Serve media files only in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
