from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.http import JsonResponse

from .models import Subscription, Subscription_Types
from .serializers import SubscriptionSerializer

@api_view(['GET'])
def subscription_detail(request, pk):
    try:
        subscription = Subscription.objects.get(pk=pk)
    except Subscription.DoesNotExist:
        return Response(status=404)

    serializer = SubscriptionSerializer(subscription)
    return Response(serializer.data)


@api_view(['GET'])
def list_subscriptions(request):
    subscription = Subscription_Types.objects.all().values('id', 'subscription_type', 'price', 'features', 'available', 'cancel')
    return JsonResponse(list(subscription), safe=False)

class SubscribeToPlan():
    def post(self, request, *args, **kwargs):
        pass
