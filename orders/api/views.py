from rest_framework.views import APIView
from orders.models import Order
from .serializers import OrdersListSerializer, OrdersPostSerializer, OrderPatchSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q

class OrdersListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get(self, request, format=None):
        """
        Retrieves a list of orders for the current user.
        """
        if request.user.is_authenticated:
            orders = Order.objects.filter(
                Q(business_user=request.user.id) | Q(customer_user=request.user.id)
        )
        else:
            orders = Order.objects.none()

        serializer = OrdersListSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Creates a new order for the current user.
        """
        serializer = OrdersPostSerializer(data=request.data)
        if self.request.user.profile.type != 'customer':
            return Response({'detail': ['Nur Kunden können Aufträge erteilen']}, status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid():
            serializer.save(customer_user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class SingleOrderAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk, format=None):  
        """
        Retrieves the order with the given primary key.
        """
        order = Order.objects.get(pk=pk)
        serializer = OrdersListSerializer(order)
        return Response(serializer.data)

    def patch(self, request, pk, format=None): 
        """
        Updates the order with the given primary key.
        """
        order = get_object_or_404(Order, pk=pk)
        is_company = order.business_user == request.user
        is_admin = request.user.is_staff
        if not (is_company or is_admin):
            return Response({"detail": ["Sie sind nicht berechtigt, diese Bestellung zu ändern."]}, status=status.HTTP_403_FORBIDDEN)
        serializer = OrderPatchSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            full_serializer = OrdersListSerializer(order)
            return Response(full_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):  # Ändere `id` zu `pk`
        """
        Deletes the order with the given primary key.
        """
        if not request.user.is_staff:
            return Response(
                {"detail": ["Sie sind nicht berechtigt, diese Bestellung zu löschen."]}, status=status.HTTP_403_FORBIDDEN)
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrdersBusinessUncompletedCountAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk, format=None): 
        """
        Retrieves the count of all uncompleted orders for a business user.
        """
        try:
            business_user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": ["Diesen Business User gibt es nicht."]}, status=status.HTTP_404_NOT_FOUND)
        orders = Order.objects.filter(business_user=business_user, status='in_progress')
        return Response({"order_count": orders.count()})

class OrdersBusinessCompletedCountAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk, format=None): 
        """
        Retrieves the count of all completed orders for a business user.
        """
        try:
            business_user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": ["Diesen Business User gibt es nicht."]}, status=status.HTTP_404_NOT_FOUND)
        orders = Order.objects.filter(business_user=business_user, status='completed')
        return Response({"completed_order_count": orders.count()})



