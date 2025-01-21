from rest_framework import serializers
from ..models import Customer, Provider

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = None  # Wähle das richtige Modell für die Vererbung.
        fields = ['username', 'email', 'password', 'type']

class CustomerSerializer(UserSerializer):
    address = serializers.CharField(max_length=255)

    class Meta(UserSerializer.Meta):
        model = Customer

class ProviderSerializer(UserSerializer):
    company_name = serializers.CharField(max_length=255)

    class Meta(UserSerializer.Meta):
        model = Provider
