from rest_framework import serializers
from orders.models import Order
from offers.models import OfferDetail

class OrdersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ['offer_detail_id']

class OrdersPostSerializer(serializers.ModelSerializer):
    offer_detail_id = serializers.PrimaryKeyRelatedField(queryset=OfferDetail.objects.all()) 

    class Meta:
        model = Order
        fields = ['offer_detail_id', 'customer_user']

    def create(self, validated_data):
        offer_detail_id = validated_data.pop('offer_detail_id')
        customer_user = validated_data.pop('customer_user')
        order = Order.objects.create(
            customer_user=customer_user.id,
            offer_detail_id=offer_detail_id,
            **validated_data
        )
        order.save()
        return order

class OrderPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


class OrderPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance








