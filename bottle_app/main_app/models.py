
from django.db import models
from django.contrib.auth.models import User
import random

class ShopItem(models.Model):
    name = models.CharField(max_length=100)
    cost = models.IntegerField()
    description = models.TextField()

class Bottle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    character_length = models.IntegerField()
    range_km = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)
    daily_read_limit = models.IntegerField(default=3)
    bottles_read_today = models.IntegerField(default=0)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    can_answer = models.BooleanField(default=False)
    bottle_read_count = models.IntegerField(default=0)

class BottleReadLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bottle = models.ForeignKey(Bottle, on_delete=models.CASCADE)
    read_at = models.DateTimeField(auto_now_add=True)

