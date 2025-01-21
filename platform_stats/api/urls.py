from django.urls import path
from .views import PlatformStatsView

urlpatterns = [
    path('platform-stats/', PlatformStatsView.as_view(), name='platform-stats'),
]
