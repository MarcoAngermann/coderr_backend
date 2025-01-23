from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from user_auth.api.serializers import ProfileSerializer, LoginSerializer , RegisterSerializer
from user_auth.models import Profile
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny

class Registration(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        
        register_serializer = RegisterSerializer(data=request.data)
        
        if register_serializer.is_valid():
            user = register_serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "token": token.key,
                    "user_id": user.id,
                    "username": user.username,
                    "email": user.email
            }, status=status.HTTP_201_CREATED
            )
        return Response(register_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Serializer-Instanz erstellen und validieren
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            # Benutzer authentifizieren
            user = authenticate(username=username, password=password)
            
            if user is not None:
                # Falls Benutzer gefunden wurde, erstelle Token
                token, created = Token.objects.get_or_create(user=user)
                data = {
                    "token": token.key,
                    "user_id": user.id,
                    "username": user.username,
                    "email": user.email
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                # Falls Benutzer nicht authentifiziert werden konnte
                return Response({"error": ["Invalid credentials"]}, status=status.HTTP_400_BAD_REQUEST)

        # Falls der Serializer ungültig ist
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfile(APIView):
    def get(self, request, id):
        try:
            profile = Profile.objects.get(user__id=id)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)



class BusinessProfiles(APIView):
    def get(self, request):
        profiles = Profile.objects.filter(type='business')
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CustomerProfiles(APIView):
    def get(self, request):
        profiles = Profile.objects.filter(type='customer')
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)














