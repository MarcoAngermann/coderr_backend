from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer, LoginSerializer
from rest_framework.authtoken.models import Token
from user_auth.models import Profile
from user_auth.api.serializers import ProfileSerializer, BusinessProfilesListSerializer, CustomerProfilesListSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import PermissionDenied


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        """
        Handles user registration by validating and saving the provided data.
        """

        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "email": user.email,
                "username": user.username,
                "user_id": user.id,
                "token": token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProfileDetailsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):  # Ändere `pk` zu `id`
        """
        Retrieves the profile details for a given primary key.
        """
        profile = get_object_or_404(Profile, user__id=id) 
        serializer = ProfileSerializer(profile)
        data = serializer.data
        data.pop('uploaded_at', None)
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request, id, format=None):  
        """
        Updates allowed fields of a profile and includes the user in the response.
        """
        profile = get_object_or_404(Profile, user__id=id) 
        if profile.user != request.user:
            raise PermissionDenied("Sie haben keine Berechtigung, dieses Profil zu ändern.")
        allowed_fields = {'email', 'first_name', 'last_name', 'file', 'location', 'description', 'working_hours', 'tel', 'username'}
        invalid_fields = [key for key in request.data if key not in allowed_fields]
        if invalid_fields:
            return Response({"detail": [f"Die Felder {', '.join(invalid_fields)} sind nicht erlaubt."]}, status=status.HTTP_400_BAD_REQUEST)
        data = {key: value for key, value in request.data.items() if key in allowed_fields}
        serializer = ProfileSerializer(profile, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({**{key: serializer.data[key] for key in data}, "user": id}, status=status.HTTP_200_OK)

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        """
        Handles user login by validating and returning the authentication token.
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({
                "user_id": serializer.validated_data["user_id"],
                "token": serializer.validated_data["token"],
                "username": serializer.validated_data["username"],
                "email": serializer.validated_data["email"],
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProfileListCustomers(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = None
    def get(self, request):
        """
        Retrieves a list of customer profiles.

        This method fetches all profiles with the type 'customer' from the database, 
        serializes the data using `ProfilesListSerializer`, and returns the serialized
        data with an HTTP 200 status code.

        :param request: The HTTP request object.
        :return: A Response object containing the serialized customer profiles data 
                with an HTTP 200 status code.
        """

        profiles = Profile.objects.filter(type='customer')
        serializer = CustomerProfilesListSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ProfileListBusiness(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = None
    def get(self, request):
        """
        Retrieves a list of business profiles.
        """

        profiles = Profile.objects.filter(type='business')
        serializer = BusinessProfilesListSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)












