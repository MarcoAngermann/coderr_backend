from django.urls import path
from . import views

urlpatterns = [
    path('offers/', views.OfferListAPIView.as_view()),
    path('offers/<int:pk>/', views.OfferDetailsAPIView.as_view()),
    path('offerdetails/<int:pk>/', views.OfferDetailDetailsAPIView.as_view(), name='offerdetails'),
]


