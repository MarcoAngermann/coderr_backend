from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomerSerializer, ProviderSerializer

class Registration(APIView):
    def post(self, request):
        data = request.data
        user_type = data.get('type')

        if user_type == 'customer':
            serializer = CustomerSerializer(data=data)
        elif user_type == 'provider':
            serializer = ProviderSerializer(data=data)
        else:
            return Response({"error": "Invalid user type"}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

