from django.urls import path
from .views import OfferList, OfferDetailView, OfferDetailList

urlpatterns = [
    path('offers/', OfferList.as_view(), name='offer-list'),
    path('offers/<int:pk>/', OfferDetailView.as_view(), name='offer-detail'),
    path('offer-details/', OfferDetailList.as_view(), name='offer-detail-list'),
]

