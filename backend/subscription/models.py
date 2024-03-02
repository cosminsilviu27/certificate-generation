from django.db import models

from accounts.models import UserAccount

class Subscription(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    subscription_type = models.CharField(max_length=50)
    max_conversions = models.PositiveIntegerField()
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_year = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.subscription_type

class SubscriptionPlan(models.Model):
    subscription_type = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    features = models.CharField(max_length=255)
    available = models.CharField(max_length=100)
    cancel = models.CharField(max_length=40)
    # other fields as necessary

class UserSubscription(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    # other fields as necessary

class Subscription_Types(models.Model):
    subscription_type = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    features = models.CharField(max_length=255)
    available = models.CharField(max_length=100)
    cancel = models.CharField(max_length=40)

    def __str__(self):
        return self.subscription_type