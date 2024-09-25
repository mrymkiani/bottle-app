from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Bottle, ShopItem, UserProfile, BottleReadLog
from .serializers import BottleSerializer, ShopItemSerializer, UserProfileSerializer
import math
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

def haversine(lat1, lon1, lat2, lon2):
    R = 6371 
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = (math.sin(dlat / 2)**2 +
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
        (math.sin(dlon / 2)**2))
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c 

class BottleReadView(generics.RetrieveAPIView):
    queryset = Bottle.objects.all()
    serializer_class = BottleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=request.user)
        bottle = self.get_object()
        distance = haversine(user_profile.latitude, user_profile.longitude,
                             bottle.latitude, bottle.longitude)

        if distance > bottle.range_km:
            return Response({"error": "You are out of range to read this bottle."}, status=403)

        if user_profile.bottles_read_today >= user_profile.daily_read_limit:
            return Response({"error": "Daily read limit reached."}, status=403)

        BottleReadLog.objects.create(user=request.user, bottle=bottle)

        user_profile.bottles_read_today += 1
        user_profile.bottle_read_count += 1
        user_profile.coins += 1  # Reward for reading a bottle
        user_profile.save()

        return Response(self.get_serializer(bottle).data)
    
class BottleCreateView(generics.CreateAPIView):
    queryset = Bottle.objects.all()
    serializer_class = BottleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user_profile = UserProfile.objects.get(user=self.request.user)
        # Check if user has enough coins to buy a bottle
        # Assuming the price is calculated based on character_length and range_km
        price = serializer.validated_data['character_length'] * 10 + serializer.validated_data['range_km'] * 5
        
        if user_profile.coins < price:
            raise serializers.ValidationError("Not enough coins to create a bottle.")
        
        # Deduct coins and create the bottle
        user_profile.coins -= price
        user_profile.save()
        serializer.save(user=self.request.user)

class ShopItemListView(generics.ListAPIView):
    queryset = ShopItem.objects.all()
    serializer_class = ShopItemSerializer


class UserProfileCreateView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        latitude = self.request.data.get('latitude')
        longitude = self.request.data.get('longitude')
        serializer.save(user=self.request.user, latitude=latitude, longitude=longitude)


class UserRankingView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["bottle_read_count"]
