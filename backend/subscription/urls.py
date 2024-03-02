from django.urls import path
from .views import list_subscriptions

urlpatterns = [
    path('list-subscriptions/', list_subscriptions, name='list_subscriptions'),
]