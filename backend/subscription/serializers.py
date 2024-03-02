from rest_framework import serializers
from .models import Subscription, Subscription_Types

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

class Subscription_TypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription_Types
        fields = '__all__'