from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from django.contrib.auth.models import User
from user_auth.models import Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        error_messages={
            "required": "E-Mail ist erforderlich.",
            "invalid": "E-Mail ist ungültig.",
            "unique": "Benutzername oder E-Mail bereits vorhanden."
        }
    )
    username = serializers.CharField(
        required=True,
        error_messages={"unique": ["Benutzername oder Email bereits vorhanden."]}
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
    )
    repeated_password = serializers.CharField(
        write_only=True,
        required=True,
    )
    type = serializers.ChoiceField(
        choices=[('customer', 'customer'), ('business', 'business')]
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']

    def validate(self, data):
        """
        Validates the given data and returns the validated data if correct.
        """
        if User.objects.filter(username=data['username']).exists() or User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(
                {"detail": ["Benutzername oder Email bereits vorhanden."]}
            )
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError(
                {"detail": ["Passwörter stimmen nicht überein."]}
            )
        return data
    


    def create(self, validated_data):
        """
        Creates a new user with the given validated data and returns the created user.
        """
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_type = validated_data['type']
        user = User.objects.create_user(username=username, email=email, password=password)
        Profile.objects.create(user=user, email=email, type=user_type)
        return user
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        extra_kwargs = {
            'email': {'error_messages': {'blank': "Dieses Feld darf nicht leer sein.", 'required': "Dieses Feld ist erforderlich.", 'unique': "Email bereits vorhanden."}},
            'first_name': {'error_messages': {'blank': "Dieses Feld darf nicht leer sein."}},
            'last_name': {'error_messages': {'blank': "Dieses Feld darf nicht leer sein."}},
            'location': {'error_messages': {'blank': "Dieses Feld darf nicht leer sein."}},
            'description': {'error_messages': {'blank': "Dieses Feld darf nicht leer sein."}},
            'working_hours': {'error_messages': {'blank': "Dieses Feld darf nicht leer sein."}},
            'tel': {'error_messages': {'blank': "Dieses Feld darf nicht leer sein."}},
        }

    def validate(self, attrs):
        """
        Validate the incoming data to ensure only allowed fields are updated.
        """
        allowed_fields = {
            'email', 'first_name', 'last_name',
            'file', 'location', 'description', 'working_hours', 'tel', 'user'
        }
        extra_fields = [key for key in self.initial_data.keys() if key not in allowed_fields]

        if extra_fields:
            raise serializers.ValidationError(
                {"detail": f"Die Felder {', '.join(extra_fields)} können nicht aktualisiert werden. Nur die Felder {', '.join(allowed_fields)} dürfen aktualisiert werden."}
            )

        return attrs

    def update(self, instance, validated_data):
        """
        Override the update method to update only the allowed fields.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Validates the given data and returns the validated data if correct.
        """
        username = data.get("username")
        password = data.get("password")
        user = User.objects.filter(username=username).first()
        if not user:
            raise serializers.ValidationError({"detail": ["Falsche Username oder Passwort."]})
        if not user.check_password(password):
            raise serializers.ValidationError({"detail": ["Falsche Username oder Passwort."]})
        token, created = Token.objects.get_or_create(user=user)
        data['user_id'] = user.id
        data['token'] = token.key
        data['email'] = user.email
        return data
    


class BusinessProfilesListSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model = Profile
        fields = ['user', 'type', 'file', 'location', 'description', 'working_hours', 'tel']

    def to_representation(self, instance):
        """
        Customizes the representation of the serializer to include the user's first
        and last name in the user field.
        """
        representation = super().to_representation(instance)
        user_representation = representation['user']
        user_representation['pk'] = user_representation.pop('id')
        user_representation['first_name'] = instance.first_name
        user_representation['last_name'] = instance.last_name
        return representation
    
class CustomerProfilesListSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model = Profile
        fields = ['user', 'type', 'file', 'uploaded_at']

    def to_representation(self, instance):
        """
        Customizes the representation of the serializer to include the user's pk
        instead of id in the user field.
        """
        representation = super().to_representation(instance)
        user_representation = representation['user']
        user_representation['pk'] = user_representation.pop('id')
        return representation





