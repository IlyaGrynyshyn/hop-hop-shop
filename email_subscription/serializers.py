from rest_framework import serializers
from email_subscription.models import SubscribedUser


class EmailSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscribedUser
        fields = [
            "email",
        ]
