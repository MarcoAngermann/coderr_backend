from user_auth.models import Profile
from rest_framework import serializers
from django.contrib.auth.models import User

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'email', 'username', 'type', 'created_at', 'first_name', 'last_name', 'file', 'location', 'description', 'working_hours', 'tel', 'uploaded_at')

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, 
        error_messages={
            'unique': ["Email bereits vorhanden."],
            'invalid': ["E-Mail ist ungültig."],
            'required': ["E-Mail ist erforderlich."]
        }
    )
    username = serializers.CharField(
        required=True,
        error_messages={
            'unique': ["Benutzername ist bereits vorhanden."]
        }
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        error_messages={
            'required': ["Passwort ist erforderlich."],
        }
    )
    repeated_password = serializers.CharField(
        write_only=True,
        required=True,
        error_messages={
            'required': ["Passwort stimmt nicht überein."],
        }
    )
    type = serializers.ChoiceField(choices=Profile.USER_TYPES, required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'repeated_password', 'type')

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists() or User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'details': ["Benutzername oder E-Mail bereits vorhanden."]})
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({'details': ["Passwort stimmt nicht überein."]})
        return data

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        type = validated_data['type']
        user = User.objects.create_user(username=username, email=email, password=password)
        Profile.objects.create(user=user, type=type, email=user.email)
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({'details': ["Invalid Password or Username"]})

        if not user.check_password(password):
            raise serializers.ValidationError({'details': ["Invalid Password or Username"]})
        return data
        
        






