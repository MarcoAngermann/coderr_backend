from rest_framework import serializers
from reviews.models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'business_user', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'reviewer']

    def validate(self, data):
        """
        Validate the incoming data to ensure only allowed fields are updated.
        """ 
        reviewer = self.context['request'].user
        if not reviewer.is_authenticated:
            raise serializers.ValidationError({"detail": ["Nur angemeldete Nutzer können eine Bewertung abgeben."]})
        if 'reviewer' in self.initial_data and int(self.initial_data['reviewer']) != reviewer.id:
            raise serializers.ValidationError({"detail": ["Sie können nur Bewertungen für sich selbst verfassen."]})
        business_user = data.get('business_user')
        if self.instance is None and Review.objects.filter(reviewer=reviewer, business_user=business_user).exists():
            raise serializers.ValidationError({"detail": ["Es ist nur eine Bewertung pro Geschäftsprofil erlaubt."]})
        return data

    def create(self, validated_data):
        """
        Creates a new review with the given validated data and returns the created review.
        """
        validated_data['reviewer'] = self.context['request'].user
        return super().create(validated_data)
