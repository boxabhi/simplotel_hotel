from rest_framework import serializers
from .models import RoomRate, OverriddenRoomRate, Discount, DiscountRoomRate


class RoomRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomRate
        fields = '__all__'

class OverriddenRoomRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OverriddenRoomRate
        fields = '__all__'
        depth = 1

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'

class DiscountRoomRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountRoomRate
        fields = '__all__'
