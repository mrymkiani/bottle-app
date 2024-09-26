from rest_framework import serializers
from .models import *

class ShopItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopItem
        fields = '__all__'

class BottleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bottle
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'