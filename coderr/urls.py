from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('user_auth.api.urls')),
    path('api/', include('offers.api.urls')),
    path('api/', include('orders.api.urls')),
    path('api/', include('reviews.api.urls')),
    path('api/', include('baseinfo.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




