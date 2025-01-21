from rest_framework import generics
from .serializers import OfferSerializer, OfferDetailSerializer
from ..models import Offer, OfferDetail

class OfferList(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

class OfferDetailList(generics.ListCreateAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer


