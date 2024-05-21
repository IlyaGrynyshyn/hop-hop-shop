from rest_framework import viewsets
from email_subscription.serializers import EmailSubscriptionSerializer
from email_subscription.models import SubscribedUser


class EmailSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = SubscribedUser.objects.all()
    serializer_class = EmailSubscriptionSerializer
