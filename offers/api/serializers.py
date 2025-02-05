from rest_framework import serializers
from django.urls import reverse
from offers.models import Offer, OfferDetail
from django.db import models

class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type', 'id']
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def __init__(self, *args, **kwargs):


        super().__init__(*args, **kwargs)
        self.fields['delivery_time_in_days'].error_messages.update({
            'invalid': "Ungültiger Wert.",
            'min_value': "Lieferzeit muss mindestens 1 Tag sein.",
            'required': "Dieses Feld ist erforderlich."
        })
        self.fields['price'].error_messages.update({
            'invalid': "Ungültiger Preis.",
            'min_value': "Preis muss höher als 1 sein.",
            'required': "Dieses Feld ist erforderlich."
        })
        self.fields['revisions'].error_messages.update({
            'invalid': "Ungültiger Wert für Revisionen.",
            'min_value': "Revisionen müssen -1 (unbegrenzt) oder eine positive Zahl sein.",
            'required': "Dieses Feld ist erforderlich."
        })

    def validate_delivery_time_in_days(self, value):


        if value <= 0:
            raise serializers.ValidationError("Lieferzeit muss mindestens 1 Tag sein.")
        return value

    def validate_price(self, value):


        if value <= 0:
            raise serializers.ValidationError("Preis muss höher als 1 sein.")
        return value

    def validate_revisions(self, value):


        if value == 0 or value < -1:
            raise serializers.ValidationError("Revisionen müssen -1 oder eine positive Zahl sein.")
        return value

    def validate_features(self, value):


        if not value or len(value) == 0:
            raise serializers.ValidationError("Mindestens eine Feature muss vorhanden sein.")
        return value


class OfferDetailURLSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, obj):
        return reverse('offerdetails', args=[obj.id])

class OfferSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id',
            'user',
            'title',
            'image',
            'description',
            'created_at',
            'updated_at',
            'details',
            'min_price',
            'min_delivery_time',
            'user_details'
        ]
        extra_kwargs = {
            'user': {'read_only': True} 
        }

    def to_representation(self, instance):

        data = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.method == 'POST':
            data.pop('created_at', None)
            data.pop('updated_at', None)
            data.pop('min_price', None)
            data.pop('min_delivery_time', None)
            data.pop('user_details', None)
            data.pop('user')
        return data
    
    def validate(self, attrs):

        details_data = self.initial_data.get('details', [])
        errors = []
        for detail in details_data:
            detail_serializer = OfferDetailSerializer(data=detail)
            if not detail_serializer.is_valid():
                errors.append(detail_serializer.errors)

        if errors:
            raise serializers.ValidationError({"detail": [errors]})
        attrs['validated_details'] = [
            detail_serializer.validated_data for detail_serializer in 
            map(lambda d: OfferDetailSerializer(data=d), details_data) if detail_serializer.is_valid()
        ]
        return attrs

    def get_details(self, obj):

        request = self.context.get('request')
        if request and request.method == 'POST':
            return OfferDetailSerializer(obj.details.all(), many=True).data
        return OfferDetailURLSerializer(obj.details.all(), many=True).data

    def get_min_price(self, obj):
  
        return obj.details.aggregate(models.Min('price'))['price__min']

    def get_min_delivery_time(self, obj):

        return obj.details.aggregate(models.Min('delivery_time_in_days'))['delivery_time_in_days__min']

    def get_user_details(self, obj):

        user = obj.user
        return {
            "first_name": user.profile.first_name,
            "last_name": user.profile.last_name,
            "username": user.profile.username
        }
    
    def create(self, validated_data):
        """
        Creates a new Offer instance with the given validated data and associated OfferDetails.
        """

        validated_details = validated_data.pop('validated_details', [])
        offer = Offer.objects.create(**validated_data)
        for detail in validated_details:
            OfferDetail.objects.create(offer=offer, **detail)

        return offer
    
    
class SingleDetailOfOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type', 'id']

class SingleFullOfferDetailSerializer(serializers.ModelSerializer):
    details = SingleDetailOfOfferSerializer(many=True) 
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id',
            'user',
            'title',
            'image',
            'description',
            'created_at',
            'updated_at',
            'details',
            'min_price',
            'min_delivery_time',
            'user_details'
        ]

    def get_min_price(self, obj):
        return obj.details.aggregate(min_price=models.Min('price'))['min_price']

    def get_min_delivery_time(self, obj):
        return obj.details.aggregate(min_delivery=models.Min('delivery_time_in_days'))['min_delivery']

    def get_user_details(self, obj):
        user = obj.user
        return {
            "first_name": user.profile.first_name,
            "last_name": user.profile.last_name,
            "username": user.profile.username
        }
    
    def validate(self, attrs):

        details_data = self.initial_data.get('details', [])
        errors = []
        for detail in details_data:
            detail_serializer = OfferDetailSerializer(data=detail)
            if not detail_serializer.is_valid():
                errors.append(detail_serializer.errors)
        if errors:
            raise serializers.ValidationError({"detail": [errors]})
        attrs['validated_details'] = [
            detail_serializer.validated_data for detail_serializer in 
            map(lambda d: OfferDetailSerializer(data=d), details_data) if detail_serializer.is_valid()
        ]
        return attrs
    
    def update(self, instance, validated_data):

        details_data = validated_data.pop('details', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if details_data is not None:
            self._update_details(instance, details_data)
        instance.save()
        return instance

    def _update_details(self, instance, details_data):

        existing_details = {detail.id: detail for detail in instance.details.all()}
        for detail_data in details_data:
            detail_id = detail_data.get('id')
            if detail_id and detail_id in existing_details:
                self._update_detail_instance(existing_details.pop(detail_id), detail_data)
            else:
                OfferDetail.objects.create(offer=instance, **detail_data)
        for remaining_detail in existing_details.values():
            remaining_detail.delete()

    def _update_detail_instance(self, detail_instance, detail_data):

        for attr, value in detail_data.items():
            setattr(detail_instance, attr, value)
        detail_instance.save()
