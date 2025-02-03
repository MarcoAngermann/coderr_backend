from rest_framework import generics, permissions, filters
from rest_framework.exceptions import PermissionDenied
from reviews.models import Review
from .serializers import ReviewSerializer
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend


class ReviewListAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['business_user_id', 'reviewer_id']
    ordering_fields = ['updated_at', 'rating']
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_permissions(self):
        """
        Returns the list of permissions that this view requires.
        """
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def perform_create(self, serializer):
        """
        Checks if the user has a customer profile before creating a review.
        """

        if not self.request.user.profile.type == 'customer':
            raise PermissionDenied(
                "Nur Benutzer mit einem Kundenprofil können Bewertungen erstellen.")
        serializer.save(reviewer=self.request.user)


class ReviewDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        """
        Returns the list of permissions that this view requires.
        """
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_update(self, serializer):
        """
        Checks if the user has permission to update a review.
        """
        if serializer.instance.reviewer != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied(
                "Nur der Ersteller oder ein Admin kann eine Bewertung bearbeiten.")
        serializer.save()

    def perform_destroy(self, instance):
        """
        Checks if the user has permission to delete a review.
        """
        if instance.reviewer != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied(
                "Nur der Ersteller oder ein Admin kann eine Bewertung löschen.")
        instance.delete()

    def update(self, request, *args, **kwargs):
        """
        Updates a review.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
