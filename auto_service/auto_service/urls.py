from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Auth
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', RedirectView.as_view(url='/profile/', permanent=False), name='account_profile'),
    
    # Local Apps
    path('', include('dashboard.urls')),
    path('services/', include('services.urls')),
    path('cars/', include('cars.urls')),
    path('bookings/', include('bookings.urls')),
    path('calculator/', include('calculator.urls')),
    path('reports/', include('reports.urls')),
    path('notifications/', include('notifications.urls', namespace='notifications')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
