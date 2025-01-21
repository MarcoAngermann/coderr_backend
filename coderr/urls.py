from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('user_auth.api.urls')),
    path('api/offers/', include('offers.api.urls')),
    path('api/orders/', include('orders.api.urls')),
    path('api/reviews/', include('reviews.api.urls')),
    path('api/platform/', include('platform_stats.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



